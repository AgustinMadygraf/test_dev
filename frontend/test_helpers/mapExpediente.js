// Test helper: pure JS implementation of mapExpediente used for unit tests
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

module.exports = { mapExpediente };
