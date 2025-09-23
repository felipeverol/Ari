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
    if os.path.exists("backend/utils/RAG/data"):
        shutil.move("backend/utils/RAG/data", "backend/utils/RAG/tmp")

    global TEST_PDF_PATH
    with open("backend/test/test.pdf", "rb") as file:
        pdf_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.pdf", pdf_file, "application/pdf")
                }
        )
    TEST_PDF_PATH = response.json()["file_path"]

    global TEST_MD_PATH
    with open("backend/test/test.md", "rb") as file:
        md_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.md", md_file, "text/markdown")
                }
        )
    TEST_MD_PATH = response.json()["file_path"]

    ####    Etapa de Run    ####
    yield

    ####    Etapa de Teardown    ####
    try:
        shutil.rmtree("backend/utils/RAG/data")
    except:
        print("Diretório inexistente")
        
    if os.path.exists("backend/utils/RAG/tmp"):
        shutil.move("backend/utils/RAG/tmp", "backend/utils/RAG/data")
    

################    Etapa de Run    ################

# deve funcionar
def test_process_pdf():
    """
    Testa se um pdf é processado corretamente
    """
    response = client.post(
        "/process-pdf",
        json={
            "file_path": TEST_PDF_PATH
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Documento processado com sucesso!"

def test_process_md():
    """
    Testa se um markdown é processado corretamente
    """
    response = client.post(
        "/process-pdf",
        json={
            "file_path": TEST_MD_PATH
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Documento processado com sucesso!"

# devem retornar erro
def test_process_non_existing_file():
    """
    Testa se um arquivo inexistente levanta erro ao ser processado
    """
    response = client.post(
        "/process-pdf",
        json={
            "file_path": "backend/utils/RAG/data/nonExisting.pdf"
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Arquivo não encontrado."

def test_process_none_file():
    """
    Testa se um caminho None levanta erro ao ser processado
    """
    response = client.post(
        "/process-pdf",
        json={
            "file_path": None
            }
    )

    # Verifica se os campos correspondem ao informado
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Arquivo não encontrado."
