from typing import Optional
from supabase_client import supabase


class UserService:
    @staticmethod
    def get_user_information(user_id: str) -> dict:
        profile = UserService._get_profile(user_id)
        if not profile:
            raise ValueError(f"Profile not found for user_id={user_id}")

        name = profile.get("name")
        email = profile.get("email")
        role = profile.get("role")

        return {
            "name": name,
            "email": email,
            "role": role,
            "school": UserService._get_school_name(user_id, role),
        }

    @staticmethod
    def _get_profile(user_id: str) -> dict | None:
        result = (
            supabase.table("profile")
            .select("name, role, email")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return result.data

    @staticmethod
    def _get_school_name(user_id: str, role: str) -> Optional[str]:
        table_map = {
            "teacher": ("teacher_class", "teacher_id"),
            "student": ("student_class", "student_id"),
        }

        if role not in table_map:
            return None

        table, fk = table_map[role]

        result = (
            supabase.table(table)
            .select("class(school(name))")
            .eq(fk, user_id)
            .limit(1)
            .single()
            .execute()
        )

        try:
            return result.data["class"]["school"]["name"]
        except (TypeError, KeyError):
            return None