// index.js

document.querySelectorAll('.flag-button').forEach(button => {
    button.addEventListener('click', () => {
        const selectedLanguage = button.dataset.language;

        // Redirect to game.html with the selected language as a query parameter
        window.location.href = `category.html?language=${selectedLanguage}`;
    });
});
