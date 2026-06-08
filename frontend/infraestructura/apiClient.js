/* Path: frontend/infraestructura/apiClient.js */
export class ApiClient {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = { ...options.headers };
        const token = localStorage.getItem('access_token');
        if (token && !headers['Authorization']) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        try {
            const response = await fetch(url, { ...options, headers });
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                if (window.location.pathname !== '/login') window.location.href = '/login';
                throw new Error('Sesión expirada');
            }
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                // Manejo mejorado de errores de validación de FastAPI (422)
                if (response.status === 422 && Array.isArray(errorData.detail)) {
                    const msg = errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
                    throw new Error(`Error de validación: ${msg}`);
                }
                throw new Error(errorData.detail || `Error: ${response.status}`);
            }
            return response.status === 204 ? null : await response.json();
        } catch (error) {
            console.error(`[ApiClient] Error en ${url}:`, error);
            throw error;
        }
    }
    get(endpoint, options = {}) { return this.request(endpoint, { ...options, method: 'GET' }); }
    post(endpoint, body, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...options.headers },
            body: JSON.stringify(body)
        });
    }
    patch(endpoint, body, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: "PATCH",
            headers: { "Content-Type": "application/json", ...options.headers },
            body: JSON.stringify(body)
        });
    }
    delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: "DELETE" });
    }
    postForm(endpoint, formData, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded', ...options.headers },
            body: formData
        });
    }
}
export const apiClient = new ApiClient();
