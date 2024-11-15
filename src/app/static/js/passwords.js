function validateForm() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const errorElement = document.getElementById('password_match_error');
    
    if (password !== confirmPassword) {
        errorElement.style.display = 'block';
        return false;
    }
    errorElement.style.display = 'none';
    return true;
}

document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;

    if (path.includes('/login')) {
        document.getElementById('login-form').addEventListener('focusin', function() {
            const errorElement = document.getElementById('wrong_password_error');
            errorElement.style.display = 'none';
        });
    } else if (path.includes('/register')) {
        document.getElementById('register-form').addEventListener('focusin', function() {
            const errorElement = document.getElementById('password_match_error');
            errorElement.style.display = 'none';
        });
    }
}, false);
