export class Expediente {
    constructor(apiData) {
        this.id = apiData.id;
        this.numero = apiData.numero || apiData.numero_referencia;
        this.extracto = apiData.extracto || apiData.resumen;
        this.descripcion = apiData.descripcion || apiData.descripcion_detallada || null;
        this.estado = apiData.estado || apiData.estado_actual;
        this.fecha_creacion = apiData.fecha_creacion || apiData.fecha_apertura;
        this.id_propietario = apiData.id_propietario;
        this.es_editable = apiData.es_editable || false;
    }
    static fromApi(data) {
        return Array.isArray(data) ? data.map(item => new Expediente(item)) : new Expediente(data);
    }
}
