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
    TEST_PDF_PATH = "backend/test/test.pdf"

    global TEST_MD_PATH
    TEST_MD_PATH = "backend/test/test.md"

    global TEST_TXT_PATH
    TEST_TXT_PATH = "backend/test/test.txt"

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
def test_save_pdf_to_non_existing_path():
    """
    Testa se um pdf é adicionado quando o diretório não existe
    """
    with open(TEST_PDF_PATH, "rb") as file:
        pdf_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.pdf", pdf_file, "application/pdf")
                }
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Arquivo salvo localmente com sucesso!"
    assert data["file_path"] == "backend/utils/RAG/data/test.pdf"
    assert data["created_data_directory"] == True

    shutil.rmtree("backend/utils/RAG/data")

def test_save_md_to_non_existing_path():
    """
    Testa se um markdown é adicionado quando o diretório não existe
    """
    with open(TEST_MD_PATH, "rb") as file:
        md_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.md", md_file, "text/markdown")
                }
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Arquivo salvo localmente com sucesso!"
    assert data["file_path"] == "backend/utils/RAG/data/test.md"
    assert data["created_data_directory"] == True

    os.remove("backend/utils/RAG/data/test.md")


def test_save_pdf_to_empty_directory():
    """
    Testa se um pdf é salvo corretamente no diretório vazio
    """
    with open(TEST_PDF_PATH, "rb") as file:
        pdf_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.pdf", pdf_file, "application/pdf")
                }
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Arquivo salvo localmente com sucesso!"
    assert data["file_path"] == "backend/utils/RAG/data/test.pdf"
    assert data["created_data_directory"] == False

    os.remove("backend/utils/RAG/data/test.pdf")

def test_save_md_to_empty_directory():
    """
    Testa se um markdown é salvo corretamente no diretório vazio
    """
    with open(TEST_MD_PATH, "rb") as file:
        md_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.md", md_file, "text/markdown")
                }
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Arquivo salvo localmente com sucesso!"
    assert data["file_path"] == "backend/utils/RAG/data/test.md"
    assert data["created_data_directory"] == False


def test_save_pdf_to_non_empty_directory():
    """
    Testa se um pdf é salvo corretamente no diretório vazio
    """
    with open(TEST_PDF_PATH, "rb") as file:
        pdf_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.pdf", pdf_file, "application/pdf")
                }
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Arquivo salvo localmente com sucesso!"
    assert data["file_path"] == "backend/utils/RAG/data/test.pdf"
    assert data["created_data_directory"] == False

def test_save_md_to_non_empty_directory():
    """
    Testa se um markdown é salvo corretamente no diretório vazio
    """
    with open(TEST_MD_PATH, "rb") as file:
        md_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.md", md_file, "text/markdown")
                }
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Arquivo salvo localmente com sucesso!"
    assert data["file_path"] == "backend/utils/RAG/data/test.md"
    assert data["created_data_directory"] == False


# def test_save_none_filetype():
#     """
#     Testa se um tipo com None levanta erro ao ser adicionado
#     """
#     with open(TEST_PDF_PATH, "rb") as file:
#         pdf_file = file.read()
#         response = client.post(
#             "/save-pdf",
#             files={
#                 "file": ("test.pdf", pdf_file, None)
#                 }
#         )

#     assert response.status_code == 200
#     data = response.json()
#     assert data["message"] == "Arquivo salvo localmente com sucesso!"
#     assert data["file_path"] == "backend/utils/RAG/data/test.pdf"
#     assert data["created_data_directory"] == False
# TODO: este teste deveria dar erro, implementar verificação de tipo

# devem retornar erro
def test_save_txt():
    """
    Testa se um txt levanta erro ao ser adicionado
    """
    with open(TEST_TXT_PATH, "rb") as file:
        txt_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": ("test.txt", txt_file, "application/txt")
                }
        )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Apenas arquivos PDF ou Markdown são permitidos."

def test_save_none_file():
    """
    Testa se um None levanta erro ao ser adicionado
    """
    response = client.post(
        "/save-pdf",
        files={
            "file": None
            }
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "There was an error parsing the body"

def test_save_none_filename():
    """
    Testa se um nome None levanta erro ao ser adicionado
    """
    with open(TEST_PDF_PATH, "rb") as file:
        pdf_file = file.read()
        response = client.post(
            "/save-pdf",
            files={
                "file": (None, pdf_file, "application/pdf")
                }
        )

    assert response.status_code == 422

def test_save_none_filecontent():
    """
    Testa se um arquivo com None levanta erro ao ser adicionado
    """
    response = client.post(
        "/save-pdf",
        files={
            "file": ("test.pdf", None, "application/pdf")
            }
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "There was an error parsing the body"

# def test_save_pdf_without_extension():
#     """
#     Testa se um pdf sem extensão é adicionado corretamente
#     """
#     with open(TEST_PDF_PATH, "rb") as file:
#         pdf_file = file.read()
#         response = client.post(
#             "/save-pdf",
#             files={
#                 "file": ("test", pdf_file, "application/pdf")
#                 }
#         )

#     assert response.status_code == 200
#     data = response.json()
#     assert data["message"] == "Arquivo salvo localmente com sucesso!"
#     assert data["file_path"] == "backend/utils/RAG/data/test"
#     assert data["created_data_directory"] == False
# TODO: este teste deveria dar certo, implementar verificação para PDF