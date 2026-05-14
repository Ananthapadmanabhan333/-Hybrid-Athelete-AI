// Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Tab switching
const authTabs = document.querySelectorAll('.auth-tab');
const authForms = document.querySelectorAll('.auth-form');

authTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;

        // Update active tab
        authTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Show corresponding form
        authForms.forEach(form => {
            if (form.id === `${targetTab}-form`) {
                form.classList.remove('hidden');
            } else {
                form.classList.add('hidden');
            }
        });
    });
});

// Password toggle
const togglePasswordButtons = document.querySelectorAll('.toggle-password');

togglePasswordButtons.forEach(button => {
    button.addEventListener('click', () => {
        const input = button.previousElementSibling;

        if (input.type === 'password') {
            input.type = 'text';
            button.textContent = 'Hide';
        } else {
            input.type = 'password';
            button.textContent = 'Show';
        }
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));

        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Helper function to show messages
function showMessage(message, type = 'info') {
    const existingMessage = document.querySelector('.auth-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `auth-message auth-message-${type}`;
    messageDiv.textContent = message;

    const authCard = document.querySelector('.auth-card');
    authCard.insertBefore(messageDiv, authCard.firstChild);

    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Sign In Form Submission
document.getElementById('signin-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('signin-email').value;
    const password = document.getElementById('signin-password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');

    // Disable button during request
    submitBtn.disabled = true;
    submitBtn.textContent = 'SIGNING IN...';

    try {
        // Create form data for OAuth2 password flow
        const formData = new URLSearchParams();
        formData.append('grant_type', 'password');
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login/access-token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Store token
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token_type', data.token_type);

            showMessage('Login successful! Redirecting...', 'success');

            // Redirect to main app after 1 second
            setTimeout(() => {
                window.location.href = 'http://localhost:8080';
            }, 1000);
        } else {
            showMessage(data.detail || 'Login failed. Please check your credentials.', 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'SIGN IN';
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('Unable to connect to server. Please ensure the backend is running.', 'error');
        submitBtn.disabled = false;
        submitBtn.textContent = 'SIGN IN';
    }
});

// Register Form Submission
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');

    // Validate passwords match
    if (password !== confirm) {
        showMessage('Passwords do not match', 'error');
        return;
    }

    // Validate password strength
    if (password.length < 8) {
        showMessage('Password must be at least 8 characters', 'error');
        return;
    }

    // Disable button during request
    submitBtn.disabled = true;
    submitBtn.textContent = 'CREATING ACCOUNT...';

    try {
        const response = await fetch(`${API_BASE_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password,
                full_name: name,
                is_superuser: false,
                is_active: true,
                dob: "1990-01-01",
                height_cm: 175,
                current_weight_kg: 75,
                activity_level: "Moderate"
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Account created successfully! Please sign in.', 'success');

            // Switch to sign in tab after 1.5 seconds
            setTimeout(() => {
                document.querySelector('[data-tab="signin"]').click();
                document.getElementById('signin-email').value = email;
            }, 1500);

            // Reset form
            e.target.reset();
        } else {
            showMessage(data.detail || 'Registration failed. Email may already be in use.', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showMessage('Unable to connect to server. Please ensure the backend is running.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'CREATE ACCOUNT';
    }
});

// Navbar scroll effect
let lastScroll = 0;
const nav = document.querySelector('.nav');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        nav.style.background = 'rgba(10, 10, 10, 0.98)';
    } else {
        nav.style.background = 'rgba(10, 10, 10, 0.95)';
    }

    lastScroll = currentScroll;
});

// Check if user is already logged in
window.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        // User is logged in, show option to go to app
        const authCard = document.querySelector('.auth-card');
        const loggedInMessage = document.createElement('div');
        loggedInMessage.className = 'auth-message auth-message-success';
        loggedInMessage.innerHTML = `
            You're already logged in. 
            <a href="http://localhost:8080" style="color: white; text-decoration: underline;">Go to App</a>
        `;
        authCard.insertBefore(loggedInMessage, authCard.firstChild);
    }
});
