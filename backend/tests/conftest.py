import pytest
# import os
from fastapi.testclient import TestClient
# from supabase import create_client
from app import app

# @pytest.fixture(scope='session')
# def test_supabase_client():
#     """
#     Retorna uma instância do cliente Supabase para testes.
#     """
#     SUPABASE_URL = os.getenv("SUPABASE_URL")
#     SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE")

#     return create_client(SUPABASE_URL, SUPABASE_KEY)

@pytest.fixture(scope='function')
def test_client():
    """
    Retorna um cliente de teste para a aplicação FastAPI.
    """
    return TestClient(app)