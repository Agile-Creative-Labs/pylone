document.addEventListener('DOMContentLoaded', function () 
{
    const button = document.getElementById('fetch-data');
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    if (button) { // Check if the button exists
        button.addEventListener('click', function () {
            if (loadingDiv) loadingDiv.style.display = 'block';
            if (errorDiv) errorDiv.style.display = 'none';
            fetch('/ajax/data')
                .then(response => response.json())
                .then(data => {
                    if(resultDiv) resultDiv.innerHTML = `<p>${data.data.message}</p>`;
                })
                .catch(error => {
                    console.error('Error:', error);
                    if (errorDiv) errorDiv.style.display = 'block';
                })
                .finally(() => {
                    if (loadingDiv) loadingDiv.style.display = 'none';
                });
        });
    }
});