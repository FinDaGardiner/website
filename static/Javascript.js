// function that allows to choose font size and saves it
function changeFontSize(size) {
    let sizeValue;
    switch (size) {
        case 'small':
            sizeValue = '12px';
            break;
        case 'medium':
            sizeValue = '16px';
            break;
        case 'large':
            sizeValue = '20px';
            break;
        default:
            sizeValue = '16px';
    }
    document.body.style.fontSize = sizeValue;
    localStorage.setItem('fontSize', sizeValue);
}

// loads the font size chosen
function loadFontSizePreference() {
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.body.style.fontSize = savedFontSize;
    }
}

// makes the changes when the page is loaded onto
window.onload = loadFontSizePreference;
