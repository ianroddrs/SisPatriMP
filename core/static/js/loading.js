const loading = document.getElementById('loading')

function showLoading() {
    loading.style.display = 'flex'
    window.addEventListener('unload', function(){});
    window.addEventListener('beforeunload', function(){});
}

function hideLoading() {
    loading.style.display = 'none'
}
  
window.onbeforeunload = function (e) {showLoading()};
window.addEventListener('load', hideLoading)