from supabase_client import supabase

class SchoolService:

    @staticmethod
    def create_school(
        name: str,
        address: str | None = None
    ):
        return supabase.table("school").insert({
            "name": name,
            "address": address,
        }).execute()