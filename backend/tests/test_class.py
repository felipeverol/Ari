import os

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
student_email = os.getenv("STUDENT_EMAIL")
student_password = os.getenv("STUDENT_PASSWORD")

def test_create_class_as_admin(test_client):
    """
    Testa o endpoint de criar turmas como admin.
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
        "/class/create",
        json={
            "school_id": "f5256e79-997a-4457-a1d2-9a91ba5cb6ac",
            "name": "Turma Teste",
            "description": "Turma criada pela bateria de testes"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json()
    assert response.status_code == 200
    assert "data" in data
    assert len(data["data"]) > 0
    assert "id" in data["data"][0]


def test_create_class_as_non_admin(test_client):
    """
    Testa o endpoint de criar turmas como usuário comum.
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
        "/class/create",
        json={
            "school_id": "f5256e79-997a-4457-a1d2-9a91ba5cb6ac",
            "name": "Turma Teste",
            "description": "Turma criada pela bateria de testes"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado. Apenas usuários com a função 'admin' podem acessar este recurso."