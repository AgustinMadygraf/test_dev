/* Path: frontend/main.js */

// Enable verbose frontend debugging when `?debug=1` is present or `localStorage.debug='1'`
const DEBUG = new URLSearchParams(window.location.search).has('debug') || localStorage.getItem('debug') === '1';

// Map API response to frontend ViewModel (normalizes field names)
function mapExpediente(apiExp) {
    const id_propietario = apiExp.id_propietario ?? apiExp.responsable_id ?? apiExp.owner_id ?? null;
    if ((id_propietario === null || id_propietario === undefined) && DEBUG) {
        console.warn('[mapExpediente] missing owner, attempting fallbacks:', apiExp);
    }
    return {
        id: apiExp.id,
        numero: apiExp.numero,
        extracto: apiExp.extracto,
        descripcion: apiExp.descripcion ?? null,
        id_propietario: id_propietario,
        estado: apiExp.estado,
        fecha_creacion: apiExp.fecha_creacion
    };
}

// --- Infrastructure Layer: Data Access ---
class ExpedienteService {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async getExpedientes(token) {
        if (DEBUG) console.info('[ExpedienteService] getExpedientes token:', token);
        const response = await fetch(this.baseUrl, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (response.status === 401) {
            if (DEBUG) console.warn('[ExpedienteService] Unauthorized (401)');
            throw new Error('Unauthorized');
        }
        const data = await response.json();
        if (DEBUG) console.debug('[ExpedienteService] fetched', Array.isArray(data) ? data.length : 'non-array', 'items', data && data.slice ? data.slice(0,3) : data);
        return data;
    }

    async createExpediente(token, payload) {
        if (DEBUG) console.info('[ExpedienteService] createExpediente payload:', payload);
        const response = await fetch(this.baseUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            let errBody = null;
            try { errBody = await response.json(); } catch (e) { errBody = null; }
            if (DEBUG) console.error('[ExpedienteService] createExpediente error', response.status, errBody);
            throw new Error((errBody && errBody.detail) ? errBody.detail : 'Error en la petición');
        }
        const data = await response.json();
        if (DEBUG) console.debug('[ExpedienteService] createExpediente success', data);
        return data;
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
        if (DEBUG) console.debug('[ExpedienteRenderer] rendering', expedientes.length, 'items');
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
        const ownerDisplay = exp.id_propietario ?? 'N/A';
        if ((exp.id_propietario === null || exp.id_propietario === undefined) && DEBUG) console.warn('[renderer] expediente has no id_propietario', exp);
        return '<tr>' +
            '<td><span class="text-muted small">#' + exp.id + '</span></td>' +
            '<td><strong class="text-primary">' + exp.numero + '</strong></td>' +
            '<td>' + exp.extracto + '</td>' +
            '<td><span class="badge rounded-pill bg-light text-dark border">Owner: ' + ownerDisplay + '</span></td>' +
            '<td>' +
                '<button class="btn btn-sm btn-link text-decoration-none" ' +
                        'onclick="app.showDetails(\'' + exp.id + '\', \'" + exp.numero + "\', \"" + exp.extracto + "\", \"" + descEscaped + "\')">' +
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
        
        const form = document.getElementById('expedienteForm');
        if (form) form.addEventListener('submit', (e) => this.handleCreate(e));
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) logoutBtn.addEventListener('click', () => this.logout());
        this.load();
    }

    async load() {
        this.ui.toggleLoading('refreshBtn', true);
        try {
            const raw = await this.service.getExpedientes(this.token);
            this.fullData = Array.isArray(raw) ? raw.map(mapExpediente) : [];
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
            const form = document.getElementById('expedienteForm');
            if (form) form.reset();
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
