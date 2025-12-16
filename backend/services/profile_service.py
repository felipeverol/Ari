from supabase_client import supabase

class ProfileService:
    
    @staticmethod
    def create_profile(user_id, data):
        return supabase.table("profile").insert({
            "id": user_id,
            **data
        }).execute()