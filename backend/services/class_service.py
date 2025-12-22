from supabase_client import supabase

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