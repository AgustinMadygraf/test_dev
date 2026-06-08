import { expedienteService } from './infraestructura/expedienteService.js';
import { authService } from './infraestructura/authService.js';
import { ExpedienteRenderer } from './ui/expedienteRenderer.js';
import { Expediente } from './dominio/expediente.js';
import { UIUtils } from './ui/uiUtils.js';

class ExpedienteApp {
    constructor() {
        this.ui = new ExpedienteRenderer();
        this.fullData = [];
        this.currentPage = 1;
        this.itemsPerPage = 5;
        this.editModal = typeof bootstrap !== 'undefined' ? new bootstrap.Modal(document.getElementById('editModal')) : null;
    }

    async init() {
        if (!authService.isAuthenticated()) {
            window.location.href = '/login';
            return;
        }

        this.setupEventListeners();
        await this.load();
    }

    setupEventListeners() {
        document.getElementById('expedienteForm')?.addEventListener('submit', (e) => this.handleCreate(e));
        document.getElementById('logoutBtn')?.addEventListener('click', () => authService.logout());
        document.getElementById('refreshBtn')?.addEventListener('click', () => this.load());
        
        document.getElementById('expedientesTableBody')?.addEventListener('click', (e) => {
            const btnDetalle = e.target.closest('.detalle-btn');
            if (btnDetalle) this.ui.showDetailsModal(btnDetalle.dataset.numero, btnDetalle.dataset.extracto, btnDetalle.dataset.descripcion);
            
            const btnDelete = e.target.closest('.delete-btn');
            if (btnDelete) this.handleDelete(btnDelete.dataset.id);
            
            const btnEdit = e.target.closest('.edit-btn');
            if (btnEdit) this.openEditModal(btnEdit);
        });

        document.getElementById('saveEditBtn')?.addEventListener('click', () => this.handleSaveEdit());

        document.getElementById('paginationContainer')?.addEventListener('click', (e) => {
            const btn = e.target.closest('.pagination-btn');
            if (btn) this.changePage(Number(btn.dataset.page));
        });
    }

    async load() {
        UIUtils.setLoading('refreshBtn', true);
        try {
            const raw = await expedienteService.getAll();
            this.fullData = Expediente.fromApi(raw);
            this.currentPage = 1;
            this.renderPage();
        } catch (err) {
            this.ui.showToast(err.message, true);
        } finally {
            UIUtils.setLoading('refreshBtn', false);
        }
    }

    renderPage() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const paginatedData = this.fullData.slice(start, start + this.itemsPerPage);
        const totalPages = Math.ceil(this.fullData.length / this.itemsPerPage);
        this.ui.renderTable(paginatedData, this.currentPage, totalPages);
    }

    changePage(page) {
        if (page < 1 || page > Math.ceil(this.fullData.length / this.itemsPerPage)) return;
        this.currentPage = page;
        this.renderPage();
    }

    async handleCreate(e) {
        e.preventDefault();
        const payload = {
            numero: document.getElementById('numero').value,
            extracto: document.getElementById('extracto').value,
            descripcion: document.getElementById('descripcion').value || null
        };

        UIUtils.setLoading('submitBtn', true);
        try {
            await expedienteService.create(payload);
            this.ui.showToast('Creado con éxito');
            e.target.reset();
            await this.load();
        } catch (err) {
            this.ui.showToast(err.message, true);
        } finally {
            UIUtils.setLoading('submitBtn', false);
        }
    }

    async handleDelete(id) {
        if (!confirm('¿Seguro que querés eliminar este expediente?')) return;
        try {
            await expedienteService.delete(id);
            this.ui.showToast('Eliminado con éxito');
            await this.load();
        } catch (err) {
            this.ui.showToast(err.message, true);
        }
    }

    openEditModal(btn) {
        document.getElementById('editId').value = btn.dataset.id;
        document.getElementById('editExtracto').value = btn.dataset.extracto;
        if (this.editModal) this.editModal.show();
    }

    async handleSaveEdit() {
        const id = document.getElementById('editId').value;
        const payload = { extracto: document.getElementById('editExtracto').value };
        
        try {
            await expedienteService.update(id, payload);
            this.ui.showToast('Actualizado con éxito');
            if (this.editModal) this.editModal.hide();
            await this.load();
        } catch (err) {
            this.ui.showToast(err.message, true);
        }
    }
}

const app = new ExpedienteApp();
document.addEventListener('DOMContentLoaded', () => app.init());
