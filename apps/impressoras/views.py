import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures # Importa para execução paralela

# Lista de impressoras
IMPRESSORAS = {
    'kyocera': [
        'http://192.168.20.56',
        'http://192.168.20.54',
        'http://196.168.20.50',
        'http://192.168.20.64',
        'http://192.168.20.193',
        'http://192.168.20.191',
        'http://192.168.20.189',
        'http://192.168.20.175',
        'http://192.168.20.169',
        'http://192.168.20.164',
        'http://192.168.20.162',
        'http://192.168.20.160',
        'http://192.168.20.159',
        'http://192.168.20.157',
        'http://192.168.20.152',
        'http://192.168.20.148',
        'http://192.168.20.147',
        'http://192.168.20.136',
        'http://192.168.20.128',
        'http://192.168.20.103',
        'http://192.168.20.234',
        'http://192.168.20.228',
        'http://192.168.20.227',
        'http://192.168.20.224',
        'http://192.168.20.213',
        'http://192.168.20.209',
    ]
}

REQUEST_TIMEOUT = 15 # Tempo limite para requisições HTTP e carregamento de página do Selenium

def parse_printer_html(html_content):
    """
    Simula a função parsePrinterHtml do JavaScript, usando Beautiful Soup.
    Retorna o conteúdo do toner ou uma mensagem de aviso.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    toner_tab_element = soup.find(id='tonertab')

    if toner_tab_element:
        next_element = toner_tab_element.find_next_sibling()
        if next_element and next_element.name == 'td':
            texto = next_element.get_text(strip=True)
            return texto
        else:
            return "Aviso: Elemento 'tonertab' encontrado, mas próximo TD não encontrado ou não é TD."
    else:
        return "Aviso: Elemento 'tonertab' não encontrado na página."

def check_printer_status(url, tipo_impressora):
    """
    Função auxiliar para verificar o status de uma única impressora.
    Será executada em paralelo para impressoras Kyocera.
    """
    status = "OK"
    content = ""
    log_message = ""
    driver = None # Inicializa o driver como None para cada thread

    try:
        if tipo_impressora == 'kyocera':
            # Configurações do Chrome para rodar em modo headless (sem interface gráfica)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox") # Essencial para alguns ambientes Linux
            chrome_options.add_argument("--disable-dev-shm-usage") # Resolve problemas de memória em alguns Docker/Linux
            chrome_options.add_argument("--log-level=3") # Suprime logs desnecessários
            chrome_options.add_argument("--window-size=1920,1080") # Define o tamanho da janela

            # Inicializa o WebDriver do Chrome para esta thread
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            driver.set_page_load_timeout(REQUEST_TIMEOUT) # Tempo limite para carregamento da página

            driver.get(url)
            wait = WebDriverWait(driver, REQUEST_TIMEOUT) # Espera explícita

            try:
                # Espera até que o frame 'wlmframe' esteja presente e mude para ele
                iframe_wlm = wait.until(EC.presence_of_element_located((By.NAME, 'wlmframe')))
                driver.switch_to.frame(iframe_wlm)

                # Espera até que o frame 'toner' esteja presente e mude para ele
                iframe_toner = wait.until(EC.presence_of_element_located((By.NAME, 'toner')))
                driver.switch_to.frame(iframe_toner)

                html_content = driver.page_source
                content = parse_printer_html(html_content)
                log_message = f"Conteúdo do Frame (via Selenium): {content}"
            except (NoSuchElementException, TimeoutException):
                log_message = "Frame 'wlmframe' ou 'toner' não encontrado ou timeout. Tentando analisar a página principal."
                html_content = driver.page_source
                content = parse_printer_html(html_content)
            except Exception as frame_e:
                log_message = f"Erro ao interagir com o frame (Selenium): {frame_e}"
                html_content = driver.page_source
                content = parse_printer_html(html_content)
                status = "Sem Acesso"
            finally:
                driver.switch_to.default_content() # Sempre volta para o conteúdo padrão

        else:
            # Para outros tipos de impressoras (se houver), usa 'requests'
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            html_content = response.text
            content = parse_printer_html(html_content)
            log_message = f"Conteúdo: {content}"

        status = "OK"

    except WebDriverException as e:
        status = "Sem Acesso"
        if "timeout" in str(e).lower():
            log_message = f"Timeout do Navegador (Selenium): {e}"
        elif "cannot find" in str(e).lower() or "no such element" in str(e).lower():
            log_message = f"Elemento não encontrado (Selenium): {e}"
        else:
            log_message = f"Erro do Navegador (Selenium): {e}"
    except requests.exceptions.Timeout:
        status = "Sem Acesso"
        log_message = "Timeout de Conexão (Requests)"
    except requests.exceptions.ConnectionError:
        status = "Sem Acesso"
        log_message = "Erro de Conexão (Requests)"
    except requests.exceptions.HTTPError as e:
        status = "Sem Acesso"
        log_message = f"Erro HTTP (Requests): {e.response.status_code}"
    except requests.exceptions.RequestException as e:
        status = "Sem Acesso"
        log_message = f"Erro Inesperado (Requests): {e}"
    except Exception as e:
        status = "Sem Acesso"
        log_message = f"Erro Interno: {e}"
    finally:
        if driver:
            driver.quit() # Garante que o driver seja fechado após cada verificação

    return {
        'url': url,
        'status': status,
        'content': content,
        'log_message': log_message,
        'type': tipo_impressora
    }

@require_http_methods(["GET"])
def printers_status(request):
    results = []
    
    # Usar ThreadPoolExecutor para executar as verificações em paralelo
    # max_workers pode ser ajustado dependendo dos recursos do servidor e da rede
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_url = {executor.submit(check_printer_status, url, tipo_impressora): (url, tipo_impressora)for tipo_impressora, urls in IMPRESSORAS.items() for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url, tipo_impressora = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                # Captura exceções que ocorreram durante a execução da thread
                results.append({
                    'url': url,
                    'status': "Erro Interno",
                    'content': "",
                    'log_message': f"Erro na execução paralela: {exc}",
                    'type': tipo_impressora
                })

    # Retorna os resultados como uma resposta JSON
    return JsonResponse({'results': results})

# View para renderizar a página HTML principal
from django.shortcuts import render

def impressoras(request):
    return render(request, 'impressoras.html')
