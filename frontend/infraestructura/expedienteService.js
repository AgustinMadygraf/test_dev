/* Path: frontend/infraestructura/expedienteService.js */
import { apiClient } from './apiClient.js';
export class ExpedienteService {
    constructor() { this.endpoint = '/expedientes/'; }
    async getAll() { return await apiClient.get(this.endpoint); }
    async create(payload) { return await apiClient.post(this.endpoint, payload); }
}
export const expedienteService = new ExpedienteService();
