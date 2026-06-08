from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.infrastructure.fastapi.schemas import UsuarioCreate, UsuarioRead
from src.infrastructure.fastapi.auth_schemas import Token
from src.infrastructure.fastapi.dependencies import get_auth_use_cases
from src.aplicacion.auth import CasosUsoAutenticacion
from src.dominio.objetos_valor import CorreoElectronico

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_cases: CasosUsoAutenticacion = Depends(get_auth_use_cases)
):
    try:
        correo = CorreoElectronico(direccion=form_data.username)
        return use_cases.iniciar_sesion(
            correo=correo,
            contrasena=form_data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UsuarioCreate,
    use_cases: CasosUsoAutenticacion = Depends(get_auth_use_cases)
):
    try:
        return use_cases.registrar(
            correo=user_data.correo,
            contrasena=user_data.contrasena,
            nombre_completo=user_data.nombre_completo,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
