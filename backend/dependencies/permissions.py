from fastapi import Depends, HTTPException, Form
from dependencies.auth import get_current_user
from supabase_client import supabase

def require_teacher(user = Depends(get_current_user)):
    profile = (
        supabase
        .table("profile")
        .select("role")
        .eq("id", user.id)
        .single()
        .execute()
        .data
    )

    if profile["role"] != "teacher":
        raise HTTPException(403, "Apenas professores")

    return user


def require_teacher_in_class(
    class_id: str = Form(...),
    user = Depends(require_teacher),
):
    result = (
        supabase
        .table("teacher_class")
        .select("class_id")
        .eq("class_id", class_id)
        .eq("teacher_id", user.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(403, "Você não é professor desta turma")

    return user
