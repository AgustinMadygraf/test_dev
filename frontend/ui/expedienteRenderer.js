/* Path: frontend/ui/expedienteRenderer.js */
export class ExpedienteRenderer {
    constructor() {
        this.tbody = document.getElementById('expedientesTableBody');
        this.paginationContainer = document.getElementById('paginationContainer');
        this.toast = typeof bootstrap !== 'undefined' ? new bootstrap.Toast(document.getElementById('liveToast')) : null;
        this.modal = typeof bootstrap !== 'undefined' ? new bootstrap.Modal(document.getElementById('detallesModal')) : null;
    }
    renderTable(expedientes, currentPage, totalPages) {
        if (!this.tbody) {
            return;
        }
        if (expedientes.length === 0) {
            this.tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted">No hay expedientes.</td></tr>';
            return;
        }
        const rows = expedientes.map(exp => {
            const html = this._createRowHTML(exp);
            return html;
        }).join('');
        this.tbody.innerHTML = rows;
        this.renderPagination(currentPage, totalPages);
    }
    renderPagination(currentPage, totalPages) {
        if (!this.paginationContainer || totalPages <= 1) return;
        this.paginationContainer.innerHTML = `
            <nav><ul class="pagination pagination-sm justify-content-center">
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <button class="page-link pagination-btn" data-page="${currentPage - 1}">Anterior</button>
                </li>
                <li class="page-item disabled"><span class="page-link">Página ${currentPage} de ${totalPages}</span></li>
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <button class="page-link pagination-btn" data-page="${currentPage + 1}">Siguiente</button>
                </li>
            </ul></nav>`;
    }
    _createRowHTML(exp) {
        const escape = (s) => String(s).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[m]));
        // Debugging the property access
        const actions = exp.es_editable 
            ? `<button class="btn btn-sm btn-outline-primary edit-btn" data-id="${exp.id}" data-extracto="${escape(exp.extracto)}" data-descripcion="${escape(exp.descripcion || '')}">✏️</button> 
               <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${exp.id}">🗑️</button>`
            : '';
        return `<tr>
            <td><span class="text-muted small">#${exp.id}</span></td>
            <td><strong class="text-primary">${escape(exp.numero)}</strong></td>
            <td>${escape(exp.extracto)}</td>
            <td><span class="badge rounded-pill bg-light text-dark border">Owner: ${exp.id_propietario ?? 'N/A'}</span></td>
            <td><button class="btn btn-sm btn-link detalle-btn" data-numero="${escape(exp.numero)}" data-extracto="${escape(exp.extracto)}" data-descripcion="${escape(exp.descripcion || '')}">Ver más</button></td>
            <td>${actions}</td>
        </tr>`;
    }
    showToast(message, isError = false) {
        document.getElementById('toastMessage').innerText = message;
        const toastEl = document.getElementById('liveToast');
        toastEl.classList.remove('text-bg-danger', 'text-bg-success');
        toastEl.classList.add(isError ? 'text-bg-danger' : 'text-bg-success');
        if (this.toast) this.toast.show();
    }
    showDetailsModal(n, e, d) {
        document.getElementById('modalNumero').innerText = n;
        document.getElementById('modalExtracto').innerText = e;
        document.getElementById('modalDescripcion').innerText = d || 'Sin descripción.';
        if (this.modal) this.modal.show();
    }
}
