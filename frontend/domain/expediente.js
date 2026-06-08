/* Path: frontend/domain/expediente.js */
export class Expediente {
    constructor(apiData) {
        this.id = apiData.id;
        this.numero = apiData.numero;
        this.extracto = apiData.extracto;
        this.descripcion = apiData.descripcion ?? null;
        this.estado = apiData.estado;
        this.fecha_creacion = apiData.fecha_creacion;
        this.id_propietario = apiData.id_propietario ?? apiData.responsable_id ?? apiData.owner_id ?? null;
    }
    static fromApi(data) {
        return Array.isArray(data) ? data.map(item => new Expediente(item)) : new Expediente(data);
    }
}
