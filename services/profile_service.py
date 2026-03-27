from supabase_client import supabase
from models.profile_models import CreateProfileRequest, ProfileRole
from typing import List

class ProfileService:
    
    @staticmethod
    def create_profile(
        user_id: str,
        name: str,
        role: ProfileRole,
        class_ids: List[str]
    ):
        supabase.table("profile").insert({
            "id": user_id,
            "name": name,
            "role": role.value
        }).execute()

        if class_ids:
            is_teacher = role == ProfileRole.TEACHER
            table = "teacher_class" if is_teacher else "student_class"
            column = "teacher_id" if is_teacher else "student_id"

            associations = [
                {column: user_id, "class_id": c_id}
                for c_id in class_ids
            ]
            supabase.table(table).insert(associations).execute()

        return {"status": "Profile was created successfully"}            