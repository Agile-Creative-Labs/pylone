class App 
{
    constructor() 
    {
        this.resultDiv = document.getElementById('result');
        this.loadingDiv = document.getElementById('loading');
        this.errorDiv = document.getElementById('error');

        this.initEventListeners();
    }

    initEventListeners() 
    {
        const fetchDataButton = document.getElementById('fetch-data');
        const loginButton = document.getElementById('btn-login');
        const registerButton = document.getElementById('btn-register');
        const signInButton = document.getElementById('btn-sign-in');

        if (fetchDataButton) 
        {
            fetchDataButton.addEventListener('click', () => this.fetchData());
        }

        if (loginButton) 
        {
            loginButton.addEventListener('click', () => this.navigateTo('/login'));
        }

        if (registerButton) 
        {
            registerButton.addEventListener('click', () => this.navigateTo('/register'));
        }
    
        if (signInButton)
        {
            signInButton.addEventListener('click', () => this.postLogin());
        }
    }


    async fetchData() 
    {
        try {
            if (this.loadingDiv) this.loadingDiv.style.display = 'block';
            if (this.errorDiv) this.errorDiv.style.display = 'none';

            const response = await fetch('/ajax/data');
            const data = await response.json();

            if (this.resultDiv) {
                this.resultDiv.innerHTML = `<p>${data.data.message}</p>`;
            }
        } catch (error) {
            console.error('Error:', error);
            if (this.errorDiv) this.errorDiv.style.display = 'block';
        } finally {
            if (this.loadingDiv) this.loadingDiv.style.display = 'none';
        }
    }

    async postLogin() 
    {
    try {
        // Show loading and hide any previous errors
        if (this.loadingDiv) this.loadingDiv.style.display = 'block';
        if (this.errorDiv) this.errorDiv.style.display = 'none';
        
        // Get form values with validation
        const usernameElement = document.getElementById('username');
        const passwordElement = document.getElementById('password');
        
        if (!usernameElement || !passwordElement) {
            throw new Error('Login form elements not found');
        }
        
        const username = usernameElement.value.trim();
        const password = passwordElement.value;
        
        // Client-side validation
        if (!username) {
            throw new Error('Username is required');
        }
        
        if (!password) {
            throw new Error('Password is required');
        }
        
        const payload = { username, password };
        
        // Send login request
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest' // Help prevent CSRF
            },
            body: JSON.stringify(payload),
            credentials: 'same-origin' // Include cookies in the request
        });
        
        // Parse response
        let data;
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            console.error('Unexpected content type:', contentType);
            throw new Error('Unexpected response format');
        }
        
        // Handle response
        if (response.ok) {
            // Show success message if needed
            if (data.message) {
                // Optional: show a success message before redirecting
                alert(data.message);
                this.showSuccessMessage(data.message);
            }
            
            // Handle redirect
            if (data.redirect) {
                alert(data.redirect);
                window.location.href = data.redirect;
            } else {
                console.warn('No redirect URL provided in successful login response');
                window.location.href = '/dashboard'; // Fallback
            }
        } else {
            // Handle error with proper message extraction
            let errorMessage = 'Authentication failed';
            
            if (data && typeof data === 'object') {
                if (data.error) {
                    errorMessage = data.error;
                } else if (data.data && data.data.error) {
                    // Handle your JSON response structure: {status: 401, data: {error: "message"}}
                    errorMessage = data.data.error;
                }
            }
            
            this.showError(errorMessage);
        }
    } catch (error) {
        console.error('Login error:', error);
        this.showError(error.message || 'An unexpected error occurred');
    } finally {
        if (this.loadingDiv) this.loadingDiv.style.display = 'none';
    }
}

// Helper methods
    showError(message) 
    {
        if (this.errorDiv) 
        {
            this.errorDiv.textContent = message;
            this.errorDiv.style.display = 'block';
        
            // Focus back to the form for accessibility
            const firstInput = document.getElementById('username');
            if (firstInput) firstInput.focus();
        }
    }

    showSuccessMessage(message) 
    {
        // You could implement this if you want to show success messages
        // Maybe add a success div to your HTML
        const successDiv = document.getElementById('login-success');
        if (successDiv) {
            successDiv.textContent = message;
            successDiv.style.display = 'block';
        }
    }

    navigateTo(route) 
    {
        window.location.href = route;
    }
}


