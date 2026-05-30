"""
Path: src/infrastructure/fastapi/routes.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.infrastructure.fastapi.schemas import ExpedienteCreate, ExpedienteRead
from src.infrastructure.fastapi.dependencies import get_expediente_use_cases, get_current_user
from src.use_cases.expediente import ExpedienteUseCases
from src.domain.entities.user import User

router = APIRouter(prefix="/expedientes", tags=["Expedientes"])

@router.post("/", response_model=ExpedienteRead, status_code=status.HTTP_201_CREATED)
async def crear_expediente(
    data: ExpedienteCreate,
    use_cases: ExpedienteUseCases = Depends(get_expediente_use_cases),
    current_user: User = Depends(get_current_user)
):
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El usuario autenticado no posee un ID válido."
        )

    return use_cases.crear_expediente(
        numero=data.numero,
        extracto=data.extracto,
        owner_id=current_user.id,
        descripcion=data.descripcion
    )

@router.get("/", response_model=List[ExpedienteRead])
async def listar_expedientes(
    use_cases: ExpedienteUseCases = Depends(get_expediente_use_cases),
    current_user: User = Depends(get_current_user)
):
    if current_user.id is None:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ID de usuario no encontrado."
        )
    return use_cases.listar_expedientes(owner_id=current_user.id)

@router.get("/{expediente_id}", response_model=ExpedienteRead)
async def obtener_expediente(
    expediente_id: int,
    use_cases: ExpedienteUseCases = Depends(get_expediente_use_cases),
    current_user: User = Depends(get_current_user)
):
    expediente = use_cases.obtener_expediente(expediente_id)
    if not expediente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expediente no encontrado")
    
    # Verificación de propiedad: Solo el dueño puede ver su expediente
    if expediente.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para ver este expediente")
        
    return expediente
