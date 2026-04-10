from supabase_client import supabase
from services.profile_service import ProfileService
from models.profile_models import ProfileRole

class AuthService:

    @staticmethod
    def signup(
        email: str,
        password: str,
        name: str,
        role: ProfileRole,
        class_ids: list[str]
    ):
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if response.user is None:
                raise Exception("Erro ao criar usuário")
            
            user_id = response.user.id

            try:
                ProfileService.create_profile(
                    user_id=user_id,
                    name=name,
                    role=role,
                    class_ids=class_ids,
                    email=email
                )
            except Exception as e:
                print(f"[signup] erro ao criar perfil: {str(e)}")
                supabase.auth.admin.delete_user(user_id)  
                raise Exception(f"Erro ao criar perfil: {str(e)}")

            return {
                "user": response.user
            }

        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def login(
        email: str,
        password: str
    ):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.session is None:
                raise Exception("Credenciais inválidas")

            return {
                "access_token": response.session.access_token
            }

        except Exception as e:
            raise Exception(str(e))