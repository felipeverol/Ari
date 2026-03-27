from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase_client import supabase

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        user = supabase.auth.get_user(token).user
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    return user
