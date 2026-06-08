/* Path: frontend/login.js */
import { authService } from './infrastructure/authService.js';
import { UIUtils } from './ui/uiUtils.js';

document.addEventListener('DOMContentLoaded', () => {
    UIUtils.togglePassword('togglePassword', 'password');

    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        UIUtils.setLoading('loginBtn', true);
        UIUtils.showAlert('alertContainer', '');

        try {
            await authService.login(email, password);
            window.location.href = '/';
        } catch (error) {
            UIUtils.showAlert('alertContainer', error.message);
        } finally {
            UIUtils.setLoading('loginBtn', false);
        }
    });
});
