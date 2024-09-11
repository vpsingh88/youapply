// This file contains common JavaScript functions used across the application

function showFlashMessage(message, type = 'info') {
    const flashContainer = document.createElement('div');
    flashContainer.className = `flash-message ${type}`;
    flashContainer.textContent = message;
    
    document.body.insertBefore(flashContainer, document.body.firstChild);
    
    setTimeout(() => {
        flashContainer.remove();
    }, 5000);
}

// Add more common functions as needed
