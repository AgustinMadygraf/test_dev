/* Path: frontend/infrastructure/authService.js */
import { apiClient } from './apiClient.js';
export class AuthService {
    async login(username, password) {
        // Limpiar token previo para evitar headers conflictivos
        localStorage.removeItem('access_token');
        
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const data = await apiClient.postForm('/auth/login', formData);
        if (data && data.access_token) {
            localStorage.setItem('access_token', data.access_token);
        }
        return data;
    }
    async register(payload) { return await apiClient.post('/auth/register', payload); }
    logout() {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    }
    isAuthenticated() { return !!localStorage.getItem('access_token'); }
}
export const authService = new AuthService();
