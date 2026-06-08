/* Path: frontend/infraestructura/expedienteService.js */
import { apiClient } from './apiClient.js';
export class ExpedienteService {
    constructor() { this.endpoint = '/expedientes/'; }
    async getAll() { return await apiClient.get(this.endpoint); }
    async create(payload) { return await apiClient.post(this.endpoint, payload); }
    async update(id, payload) { return await apiClient.patch(`${this.endpoint}${id}`, payload); }
    async delete(id) { return await apiClient.delete(`${this.endpoint}${id}`); }
}
export const expedienteService = new ExpedienteService();
