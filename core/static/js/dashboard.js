
document.addEventListener("DOMContentLoaded", async () => {
    if (typeof window.dataManager === 'undefined') {
        console.error('DataManager is not defined. Ensure main.js is loaded before dashboard.js');
        return;
    }

    try {
        const chartData = await window.dataManager.request('/api/dashboard_charts/');

        // --- Gráfico 1: Equipamentos por Local (Barras) ---
        var optionsLocal = {
            series: [{
                name: 'Quantidade',
                data: chartData.equipamentos_por_local.series
            }],
            chart: {
                type: 'bar',
                height: 350,
                toolbar: { show: false }
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%',
                    endingShape: 'rounded'
                },
            },
            dataLabels: { enabled: false },
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            xaxis: {
                categories: chartData.equipamentos_por_local.labels,
                title: { text: 'Locais' }
            },
            yaxis: {
                title: { text: 'Nº de equipamentos' }
            },
            fill: { opacity: 1 },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val + " equipamentos";
                    }
                }
            }
        };
        var chartLocal = new ApexCharts(document.querySelector("#chart-equipamentos-local"), optionsLocal);
        chartLocal.render();

        // --- Gráfico 2: Equipamentos por Tipo (Donut) ---
        var optionsTipo = {
            series: chartData.equipamentos_por_tipo.series,
            chart: {
                type: 'donut',
                height: 350
            },
            labels: chartData.equipamentos_por_tipo.labels,
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }]
        };
        var chartTipo = new ApexCharts(document.querySelector("#chart-equipamentos-tipo"), optionsTipo);
        chartTipo.render();

        // --- Gráfico 3: Equipamentos por Fabricante (Barras Horizontais) ---
        var optionsFabricante = {
            series: [{
                data: chartData.equipamentos_por_fabricante.series
            }],
            chart: {
                type: 'bar',
                height: 350,
                toolbar: { show: false }
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: chartData.equipamentos_por_fabricante.labels,
                title: { text: 'Nº de equipamentos' }
            },
            yaxis: {
                title: { text: 'Fabricantes' }
            },
            tooltip: {
                x: {
                    formatter: function (val) {
                        return val + " equipamentos";
                    }
                }
            }
        };
        var chartFabricante = new ApexCharts(document.querySelector("#chart-equipamentos-fabricante"), optionsFabricante);
        chartFabricante.render();

        // --- Gráfico 4: Movimentações por Mês (Área) ---
        var optionsMovimentacoesMes = {
            series: [{
                name: "Movimentações",
                data: chartData.movimentacoes_por_mes.series
            }],
            chart: {
                type: 'area',
                height: 350,
                toolbar: { show: false }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            xaxis: {
                categories: chartData.movimentacoes_por_mes.labels,
                title: { text: 'Mês/Ano' }
            },
            yaxis: {
                title: { text: 'Nº de Movimentações' },
                min: 0,
                tickAmount: 5
            },
            tooltip: {
                x: {
                    format: 'dd/MM/yy HH:mm'
                },
                y: {
                    formatter: function (val) {
                        return val + " movimentações";
                    }
                }
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.7,
                    opacityTo: 0.9,
                    stops: [0, 100]
                }
            }
        };
        var chartMovimentacoesMes = new ApexCharts(document.querySelector("#chart-movimentacoes-mes"), optionsMovimentacoesMes);
        chartMovimentacoesMes.render();

    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        window.dataManager.showAlert('Erro ao carregar dados do dashboard.', 'danger');
    }
});
