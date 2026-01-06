import os

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
student_email = os.getenv("STUDENT_EMAIL")
student_password = os.getenv("STUDENT_PASSWORD")

def test_create_profile_as_admin(test_client):
    """
    Testa o endpoint de criar perfis como admin.
    """
    login_response = test_client.post(
        "/auth/login",
        json={
            "email": admin_email,
            "password": admin_password
        }
    )

    token = login_response.json()["session"]["access_token"]

    response = test_client.post(
        "/profile/create",
        json={
            "user_id": "b93a7382-a02a-4226-b4ca-cda523038d65",
            "name": "Professor Teste",
            "role": "teacher",
            "class_ids": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_create_profile_as_non_admin(test_client):
    """
    Testa o endpoint de criar perfis como usuário comum.
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
        "/profile/create",
        json={
            "user_id": "b93a7382-a02a-4226-b4ca-cda523038d65",
            "name": "Professor Teste",
            "role": "teacher",
            "class_ids": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado. Apenas usuários com a função 'admin' podem acessar este recurso."