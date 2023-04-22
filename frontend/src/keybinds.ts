const blacklistedTagNames = ['INPUT', 'SELECT', 'TEXTAREA', 'DATALIST', 'OPTION', 'OPTGROUP'];

function shouldKeybindsBeDisabled() {
    if (!document.activeElement) return false;

    let activeElement = document.activeElement;
    return (
        blacklistedTagNames.includes(activeElement.tagName) ||
        activeElement.getAttribute('editableContent') === 'true'
    );
}

function addSingleKeybind(key: string, callback: () => void) {
    document.addEventListener('keyup', (e) => {
        if (!shouldKeybindsBeDisabled() && e.key === key) {
            callback();
        }
    });
}

export { addSingleKeybind };
