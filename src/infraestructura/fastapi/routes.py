from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.infraestructura.fastapi.schemas import ExpedienteCreate, ExpedienteUpdate, ExpedienteRead
from src.infraestructura.fastapi.dependencies import get_expediente_use_cases, get_current_user
from src.aplicacion.expediente import CasosUsoExpediente
from src.dominio.entidades.usuario import Usuario

router = APIRouter(prefix="/expedientes", tags=["Expedientes"])

@router.post("/", response_model=ExpedienteRead, status_code=status.HTTP_201_CREATED)
async def crear_expediente(
    data: ExpedienteCreate,
    use_cases: CasosUsoExpediente = Depends(get_expediente_use_cases),
    current_user: Usuario = Depends(get_current_user)
):
    return use_cases.crear_expediente(
        numero=str(data.numero),
        extracto=data.extracto,
        id_propietario=current_user.id,
        descripcion=data.descripcion
    )

@router.get("/", response_model=List[ExpedienteRead])
async def listar_expedientes(
    use_cases: CasosUsoExpediente = Depends(get_expediente_use_cases),
    current_user: Usuario = Depends(get_current_user)
):
    return use_cases.listar_expedientes(id_propietario=current_user.id)

@router.get("/{expediente_id}", response_model=ExpedienteRead)
async def obtener_expediente(
    expediente_id: int,
    use_cases: CasosUsoExpediente = Depends(get_expediente_use_cases),
    current_user: Usuario = Depends(get_current_user)
):
    expediente = use_cases.obtener_expediente(expediente_id)
    if not expediente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expediente no encontrado")
    if expediente.id_propietario != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para ver este expediente")
    return expediente

@router.patch("/{expediente_id}", response_model=ExpedienteRead)
async def actualizar_expediente(
    expediente_id: int,
    data: ExpedienteUpdate,
    use_cases: CasosUsoExpediente = Depends(get_expediente_use_cases),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        return use_cases.actualizar_expediente(
            id_expediente=expediente_id,
            id_propietario=current_user.id,
            extracto=data.extracto,
            descripcion=data.descripcion
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{expediente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_expediente(
    expediente_id: int,
    use_cases: CasosUsoExpediente = Depends(get_expediente_use_cases),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        use_cases.eliminar_expediente(expediente_id, current_user.id)
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
