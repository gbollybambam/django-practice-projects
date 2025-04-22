document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.login-form form');
    const button = document.querySelector('.login-button');
    const buttonText = button.querySelector('.button-text');
    const spinner = button.querySelector('.spinner');

    form.addEventListener('submit', () => {
        buttonText.style.display = 'none';
        spinner.style.display = 'inline-block';
        button.disabled = true;
    })
});