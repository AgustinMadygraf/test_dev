"""
Path: src/infrastructure/fastapi/auth_routes.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.infrastructure.fastapi.auth_schemas import Token
from src.infrastructure.fastapi.dependencies import get_auth_use_cases
from src.use_cases.auth import AuthUseCases

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    try:
        return use_cases.login(
            email=form_data.username, 
            password=form_data.password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
