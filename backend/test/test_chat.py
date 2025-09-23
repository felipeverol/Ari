import pytest
import os
import shutil
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def set_data_before_test():
    """
    Renomeia a pasta backend/utils/RAG/data para tmp para realizar os testes e depois retorna a pasta
    """
    ####    Etapa de Setup    ####
    # TODO: setar um mock do banco de dados vetorial para os testes

    ####    Etapa de Run    ####
    yield

    ####    Etapa de Teardown    ####
    # TODO: deletar o mock criado
    

################    Etapa de Run    ################

# deve funcionar
# def test_valid_query_with_answer():
#     """
#     Testa uma pergunta que deveria ter resposta no banco de dados vetorial
#     """
#     response = client.post(
#         "/chat",
#         json={
#             "query": "pergunta" # TODO: colocar pergunta
#             }
#     )

#     assert response.status_code == 200
#     data = response.json()
#     assert data["response"] == "" # TODO: resposta esperada

# def test_valid_query_with_no_answer():
#     """
#     Testa uma pergunta que não deveria ter resposta no banco de dados vetorial
#     """
#     response = client.post(
#         "/chat",
#         json={
#             "query": "pergunta" # TODO: colocar pergunta
#             }
#     )

#     assert response.status_code == 200
#     data = response.json()
#     assert data["response"] == "" # TODO: resposta esperada

# devem retornar erro
def test_empty_query():
    """
    Testa se uma query vazia levanta um erro
    """
    response = client.post(
        "/chat",
        json={
            "query": ""
            }
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Query não fornecida."

def test_none_query():
    """
    Testa se uma query None levanta um erro
    """
    response = client.post(
        "/chat",
        json={
            "query": None
            }
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Query não fornecida."