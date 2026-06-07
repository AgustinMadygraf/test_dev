// Minimal test helper implementing _createRowHTML logic for ExpedienteRenderer
function createRowHTML(exp) {
  const descEscaped = (exp.descripcion || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
  const ownerDisplay = exp.id_propietario ?? 'N/A';
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

module.exports = { createRowHTML };
