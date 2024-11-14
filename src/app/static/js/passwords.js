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


document.addEventListener('DOMContentLoaded', function ()
{
    document.getElementById('confirm_password').addEventListener('focus', function() {
        const errorElement = document.getElementById('password_match_error');
        errorElement.style.display = 'none';
    });
    
    document.getElementById('password').addEventListener('focus', function() {
        const errorElement = document.getElementById('password_match_error');
        errorElement.style.display = 'none';
    });
}, false);