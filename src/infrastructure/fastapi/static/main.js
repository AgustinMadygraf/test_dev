/* 
 Path: src/infrastructure/fastapi/static/main.js 
 */

const API_URL = '/expedientes/';

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
    }
    loadExpedientes();
});

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
});

document.getElementById('expedienteForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        numero: document.getElementById('numero').value,
        extracto: document.getElementById('extracto').value,
        descripcion: document.getElementById('descripcion').value || null
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert('Expediente creado correctamente');
            document.getElementById('expedienteForm').reset();
            loadExpedientes();
        } else {
            const err = await response.json();
            alert('Error: ' + (err.detail || 'No se pudo crear el expediente'));
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

async function loadExpedientes() {
    const tbody = document.getElementById('expedientesTableBody');
    try {
        const response = await fetch(API_URL, {
            headers: { 
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        
        if (response.status === 401) {
            window.location.href = '/login';
            return; // Detenemos la ejecución si no está autorizado
        }
        
        const data = await response.json();
        tbody.innerHTML = data.map(exp => `
            <tr>
                <td>${exp.id}</td>
                <td><strong>${exp.numero}</strong></td>
                <td>${exp.extracto}</td>
                <td><span class="badge bg-secondary">${exp.owner_id}</span></td>
                <td><button class="btn btn-sm btn-outline-info" onclick="alert('Descripción: ' + \`${exp.descripcion || 'Sin descripción'}\`)">Detalles</button></td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error al cargar datos</td></tr>';
    }
}
