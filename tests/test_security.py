from src.infraestructura.settings.security import verificar_contrasena, obtener_hash_contrasena, crear_token_acceso, decode_access_token, JWTSecurityService
from datetime import timedelta

def test_password_hashing():
    pw = "password"
    hashed = obtener_hash_contrasena(pw)
    assert verificar_contrasena(pw, hashed)
    assert not verificar_contrasena("wrong", hashed)

def test_jwt_token():
    datos = {"sub": "test@test.com"}
    token = crear_token_acceso(datos)
    payload = decode_access_token(token)
    assert payload["sub"] == "test@test.com"

def test_decode_invalid_token():
    assert decode_access_token("invalid-token") is None

def test_jwt_service():
    service = JWTSecurityService()
    assert service.verificar_contrasena("pass", service.obtener_hash_contrasena("pass"))
