import os

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
student_email = os.getenv("STUDENT_EMAIL")
student_password = os.getenv("STUDENT_PASSWORD")

def test_login_success(test_client):
    """
    Testa o endpoint de login com credenciais válidas.
    """
    response = test_client.post(
        "/auth/login",
        json={
            "email": student_email,
            "password": student_password
        }
    )

    data = response.json()
    assert response.status_code == 200
    assert "user" in data
    assert "session" in data
    assert "access_token" in data["session"]


def test_login_failure(test_client):
    """
    Testa o endpoint de login com credenciais inválidas.
    """
    response = test_client.post(
        "/auth/login",
        json={
            "email": "invalid@email.com",
            "password": "invalidPassword"
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid login credentials"


def test_signup_without_token(test_client):
    """
    Testa o acesso a uma rota protegida sem fornecer um token.
    """
    response = test_client.post(
        "/auth/signup",
        json={
            "email": "abcd5432@gmail.com",
            "password": "testePassword"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


def test_signup_as_non_admin(test_client):
    """
    Testa o acesso a uma rota protegida com um token válido.
    """
    login_response = test_client.post(
        "/auth/login",
        json={
            "email": student_email,
            "password": student_password
        }
    )
    token = login_response.json()["session"]["access_token"]

    response = test_client.post(
        "/auth/signup",
        json={
            "email": "abcd5432@gmail.com",
            "password": "testePassword"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado. Apenas usuários com a função 'admin' podem acessar este recurso."