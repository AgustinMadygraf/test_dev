/* Deprecated copy of main.js kept for reference */
// Enable verbose frontend debugging when `?debug=1` is present or `localStorage.debug='1'`
const DEBUG = new URLSearchParams(window.location.search).has('debug') || localStorage.getItem('debug') === '1';

function mapExpediente(apiExp) {
    const id_propietario = apiExp.id_propietario ?? apiExp.responsable_id ?? apiExp.owner_id ?? null;
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

class ExpedienteService { /* ... */ }

class ExpedienteRenderer { /* ... */ }

class ExpedienteApp { /* ... */ }

const app = new ExpedienteApp();
document.addEventListener('DOMContentLoaded', () => app.init());
