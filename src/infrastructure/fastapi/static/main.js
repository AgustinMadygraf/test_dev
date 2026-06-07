/* Path: src/infrastructure/fastapi/static/main.js */

// --- Infrastructure Layer: Data Access ---
class ExpedienteService {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async getExpedientes(token) {
        const response = await fetch(this.baseUrl, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (response.status === 401) throw new Error('Unauthorized');
        return await response.json();
    }

    async createExpediente(token, payload) {
        const response = await fetch(this.baseUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error en la petición');
        }
        return await response.json();
    }
}

// --- UI Layer: Presentation ---
class ExpedienteRenderer {
    constructor() {
        this.toastEl = document.getElementById('liveToast');
        this.modalEl = document.getElementById('detallesModal');
        this.tbody = document.getElementById('expedientesTableBody');
        this.paginationContainer = document.getElementById('paginationContainer');
        
        if (typeof bootstrap !== 'undefined') {
            this.toast = this.toastEl ? new bootstrap.Toast(this.toastEl) : null;
            this.modal = this.modalEl ? new bootstrap.Modal(this.modalEl) : null;
        }
    }

    renderTable(expedientes, currentPage, totalPages) {
        if (!this.tbody) return;
        if (expedientes.length === 0) {
            this.tbody.innerHTML = '<tr><td colspan="5" class="text-center py-4 text-muted">No hay expedientes.</td></tr>';
            this.renderPagination(0, 0);
            return;
        }
        this.tbody.innerHTML = expedientes.map(exp => this._createRowHTML(exp)).join('');
        this.renderPagination(currentPage, totalPages);
    }

    renderPagination(currentPage, totalPages) {
        if (!this.paginationContainer) return;
        if (totalPages <= 1) {
            this.paginationContainer.innerHTML = '';
            return;
        }
        let html = '<nav aria-label="Navegación de expedientes">' +
            '<ul class="pagination pagination-sm justify-content-center">';
        
        html += '<li class="page-item ' + (currentPage === 1 ? 'disabled' : '') + '">' +
            '<button class="page-link" onclick="app.changePage(' + (currentPage - 1) + ')">Anterior</button>' +
            '</li>';
        
        html += '<li class="page-item disabled"><span class="page-link">Página ' + currentPage + ' de ' + totalPages + '</span></li>';
        
        html += '<li class="page-item ' + (currentPage === totalPages ? 'disabled' : '') + '">' +
            '<button class="page-link" onclick="app.changePage(' + (currentPage + 1) + ')">Siguiente</button>' +
            '</li>';
        
        html += '</ul></nav>';
        this.paginationContainer.innerHTML = html;
    }

    _createRowHTML(exp) {
        const descEscaped = (exp.descripcion || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
        return '<tr>' +
            '<td><span class="text-muted small">#' + exp.id + '</span></td>' +
            '<td><strong class="text-primary">' + exp.numero + '</strong></td>' +
            '<td>' + exp.extracto + '</td>' +
            '<td><span class="badge rounded-pill bg-light text-dark border">Owner: ' + (exp.owner_id || exp.id_propietario || exp.responsable_id) + '</span></td>' +
            '<td>' +
                '<button class="btn btn-sm btn-link text-decoration-none" ' +
                        'onclick="app.showDetails(\'' + exp.id + '\', \'' + exp.numero + '\', \'' + exp.extracto + '\', \'' + descEscaped + '\')">' +
                    'Ver más' +
                '</button>' +
            '</td>' +
        '</tr>';
    }

    showToast(message, title = 'Notificación', isError = false) {
        const titleEl = document.getElementById('toastTitle');
        const msgEl = document.getElementById('toastMessage');
        if (titleEl) titleEl.innerText = title;
        if (msgEl) msgEl.innerText = message;
        
        if (this.toastEl) {
            this.toastEl.classList.remove('text-bg-danger', 'text-bg-success');
            this.toastEl.classList.add(isError ? 'text-bg-danger' : 'text-bg-success');
        }
        if (this.toast) this.toast.show();
    }

    showDetailsModal(numero, extracto, descripcion) {
        document.getElementById('modalNumero').innerText = numero;
        document.getElementById('modalExtracto').innerText = extracto;
        document.getElementById('modalDescripcion').innerText = descripcion || 'Sin descripción adicional.';
        if (this.modal) this.modal.show();
    }

    toggleLoading(btnId, isLoading) {
        const btn = document.getElementById(btnId);
        if (!btn) return;
        const spinner = btn.querySelector('.spinner-border');
        const text = btn.querySelector('.btn-text');
        
        btn.disabled = isLoading;
        if (spinner) spinner.classList.toggle('d-none', !isLoading);
        if (text) text.classList.toggle('opacity-50', isLoading);
    }
}

// --- Application Layer: Controller ---
class ExpedienteApp {
    constructor() {
        this.service = new ExpedienteService('/expedientes/');
        this.ui = new ExpedienteRenderer();
        this.token = localStorage.getItem('access_token');
        this.fullData = [];
        this.currentPage = 1;
        this.itemsPerPage = 5;
    }

    init() {
        if (!this.token) window.location.href = '/login';
        
        document.getElementById('expedienteForm').addEventListener('submit', (e) => this.handleCreate(e));
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());
        this.load();
    }

    async load() {
        this.ui.toggleLoading('refreshBtn', true);
        try {
            this.fullData = await this.service.getExpedientes(this.token);
            this.currentPage = 1;
            this.renderPage();
        } catch (err) {
            if (err.message === 'Unauthorized') window.location.href = '/login';
            else this.ui.showToast('Error cargando datos', 'Error', true);
        } finally {
            this.ui.toggleLoading('refreshBtn', false);
        }
    }

    renderPage() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        const paginatedData = this.fullData.slice(start, end);
        const totalPages = Math.ceil(this.fullData.length / this.itemsPerPage);
        this.ui.renderTable(paginatedData, this.currentPage, totalPages);
    }

    changePage(newPage) {
        this.currentPage = newPage;
        this.renderPage();
    }

    async handleCreate(e) {
        e.preventDefault();
        this.ui.toggleLoading('submitBtn', true);
        const payload = {
            numero: document.getElementById('numero').value,
            extracto: document.getElementById('extracto').value,
            descripcion: document.getElementById('descripcion').value || null
        };
        try {
            await this.service.createExpediente(this.token, payload);
            this.ui.showToast('Creado con éxito', 'Éxito');
            document.getElementById('expedienteForm').reset();
            await this.load();
        } catch (err) {
            this.ui.showToast(err.message, 'Error', true);
        } finally {
            this.ui.toggleLoading('submitBtn', false);
        }
    }

    showDetails(id, n, e, d) { this.ui.showDetailsModal(n, e, d); }
    logout() { localStorage.removeItem('access_token'); window.location.href = '/login'; }
}

const app = new ExpedienteApp();
document.addEventListener('DOMContentLoaded', () => app.init());
