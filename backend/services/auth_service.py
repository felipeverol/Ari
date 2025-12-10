from supabase_client import supabase

class AuthService:

    @staticmethod
    def signup(email: str, password: str):
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if response.user is None:
                raise Exception("Erro ao criar usuário")

            return {
                "user": response.user
            }

        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def login(email: str, password: str):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.session is None:
                raise Exception("Credenciais inválidas")

            return {
                "session": response.session,
                "user": response.user
            }

        except Exception as e:
            raise Exception(str(e))