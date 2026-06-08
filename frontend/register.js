/* Path: frontend/register.js */
import { authService } from './infrastructure/authService.js';
import { UIUtils } from './ui/uiUtils.js';

document.addEventListener('DOMContentLoaded', () => {
    UIUtils.togglePassword('togglePassword', 'password');

    const registerForm = document.getElementById('registerForm');
    if (!registerForm) return;

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        // Ajustado para coincidir con el esquema UsuarioCreate del backend
        const payload = {
            correo: document.getElementById('email').value,
            contrasena: document.getElementById('password').value,
            nombre_completo: document.getElementById('nombre_completo').value || null
        };

        UIUtils.setLoading('registerBtn', true);
        UIUtils.showAlert('alertContainer', '');

        try {
            await authService.register(payload);
            UIUtils.showAlert('alertContainer', 'Usuario creado con éxito. Redirigiendo...', 'success');
            setTimeout(() => { window.location.href = '/login'; }, 2000);
        } catch (error) {
            UIUtils.showAlert('alertContainer', error.message);
            UIUtils.setLoading('registerBtn', false);
        }
    });
});
