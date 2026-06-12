from fastapi import APIRouter, HTTPException, status
from schemas import LoginRequest, TokenResponse
from auth import authenticate_linux_user, create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    if not authenticate_linux_user(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    token = create_access_token(data={"sub": request.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": request.username
    }