from supabase_client import supabase
from dependencies.permissions import get_user_role, ProfileRole

class ClassService:

    @staticmethod
    def create_class(
        school_id: str,
        name: str,
        description: str | None = None
    ):
        return supabase.table("class").insert({
            "school_id": school_id,
            "name": name,
            "description": description
        }).execute()
    
    @staticmethod
    def get_classes(user_id: str):
        role = get_user_role(user_id)
        if role == ProfileRole.TEACHER:
            return supabase.table("teacher_class").select("class(*)").eq("teacher_id", user_id).execute()
        elif role == ProfileRole.STUDENT:
            return supabase.table("student_class").select("class(*)").eq("student_id", user_id).execute()