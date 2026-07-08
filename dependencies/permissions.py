from fastapi import Depends, HTTPException, Form
from dependencies.auth import get_current_user
from supabase_client import supabase
from models.profile_models import ProfileRole

def get_user_role(user_id: str) -> ProfileRole:
    profile = (
        supabase
        .table("profile")
        .select("role")
        .eq("id", user_id)
        .single()
        .execute()
        .data
    )
    
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Perfil do usuário não encontrado."
        )

    return profile["role"]

def require_role(required_role: ProfileRole):
    
    def role_checker(user = Depends(get_current_user)):
        
        current_role = get_user_role(user.id)

        if current_role == ProfileRole.ADMIN:
            return user

        if current_role != required_role:
            raise HTTPException(
                status_code=403, 
                detail=f"Acesso negado. Apenas usuários com a função '{required_role.value}' podem acessar este recurso."
            )
        
        return user 
    return role_checker

def require_teacher_in_class(
    class_id: str = Form(...),
    user = Depends(require_role(ProfileRole.TEACHER)),
):
    current_role = get_user_role(user.id)
    
    if current_role == ProfileRole.ADMIN:
        return user
    
    result = (
        supabase
        .table("teacher_class")
        .select("class_id")
        .eq("class_id", class_id)
        .eq("teacher_id", user.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=403,
            detail="Você não é professor desta turma"
        )

    return user

def require_student_in_class(
    class_id: str = Form(...),
    user = Depends(require_role(ProfileRole.STUDENT)),
):
    current_role = get_user_role(user.id)
    
    if current_role == ProfileRole.ADMIN:
        return user
    
    result = (
        supabase
        .table("student_class")
        .select("class_id")
        .eq("class_id", class_id)
        .eq("student_id", user.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=403,
            detail="Você não é aluno desta turma"
        )

    return user
