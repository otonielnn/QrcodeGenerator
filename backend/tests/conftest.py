"""
Configuração comum para todos os testes
"""
import os
import sys
import tempfile

import pytest
from fastapi.testclient import TestClient
from PIL import Image

# Adicionar o diretório raiz ao path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from main import app


@pytest.fixture
def client():
    """Cliente de teste para a API FastAPI"""
    return TestClient(app)


@pytest.fixture
def sample_image():
    """Cria uma imagem de exemplo para testes"""
    img = Image.new('RGB', (100, 100), color='red')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(temp_file.name, 'PNG')
    temp_file.close()

    yield temp_file.name

    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def sample_logo_file():
    """Cria um arquivo de logo para upload nos testes"""
    img = Image.new('RGBA', (50, 50), color=(255, 0, 0, 255))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(temp_file.name, 'PNG')
    temp_file.close()

    yield temp_file.name

    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def invalid_image_file():
    """Cria um arquivo inválido para testes de erro"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
    temp_file.write("Este não é um arquivo de imagem válido")
    temp_file.close()

    yield temp_file.name

    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


# URLs de teste comuns
TEST_URLS = [
    "https://google.com",
    "https://github.com",
    "https://example.com",
    "https://python.org",
]

INVALID_URLS = [
    "",
    " ",
    "not-a-url",
    "ftp://invalid-protocol.com",
]
