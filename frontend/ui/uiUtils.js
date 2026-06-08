/* Path: frontend/ui/uiUtils.js */
export class UIUtils {
    static togglePassword(buttonId, passwordId) {
        const btn = document.getElementById(buttonId);
        const input = document.getElementById(passwordId);
        if (!btn || !input) return;
        btn.addEventListener('click', () => {
            const icon = btn.querySelector('i');
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            icon.classList.replace(isPassword ? 'bi-eye' : 'bi-eye-slash', isPassword ? 'bi-eye-slash' : 'bi-eye');
        });
    }
    static setLoading(btnId, isLoading) {
        const btn = document.getElementById(btnId);
        if (!btn) return;
        const spinner = btn.querySelector('.spinner-border');
        const text = btn.querySelector('.btn-text');
        btn.disabled = isLoading;
        if (spinner) spinner.classList.toggle('d-none', !isLoading);
        if (text) text.classList.toggle('opacity-50', isLoading);
    }
    static showAlert(containerId, message, type = 'danger') {
        const container = document.getElementById(containerId);
        if (container) container.innerHTML = `<div class="alert alert-${type} small py-2">${message}</div>`;
    }
}
