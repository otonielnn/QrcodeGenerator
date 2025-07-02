"""
Testes para as funções utilitárias de geração de QR Code
"""
import os
import sys
import tempfile

import pytest
from PIL import Image

# Adicionar o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from qrcode_utils import (
    arredondar_cantos,
    criar_moldura_arredondada,
    gerar_qrcode,
)


class TestGerarQRCode:
    """Testes para a função gerar_qrcode"""

    def test_gerar_qrcode_url_simples(self):
        """Teste: gerar QR code com URL simples"""
        url = "https://google.com"
        result = gerar_qrcode(url)

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"  # Verificar modo em vez de format
        assert result.size[0] > 0
        assert result.size[1] > 0

    def test_gerar_qrcode_url_vazia(self):
        """Teste: erro com URL vazia"""
        with pytest.raises(ValueError, match="Qrcode NÃO GERADO"):
            gerar_qrcode("")

    def test_gerar_qrcode_url_none(self):
        """Teste: erro com URL None"""
        with pytest.raises(ValueError, match="Qrcode NÃO GERADO"):
            gerar_qrcode(None)

    def test_gerar_qrcode_com_logo_valido(self, sample_image):
        """Teste: gerar QR code com logo válido"""
        url = "https://example.com"
        result = gerar_qrcode(url, logo_path=sample_image)

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"  # Verificar modo em vez de format
        # QR code com logo deve ter tamanho adequado
        assert result.size[0] > 200
        assert result.size[1] > 200

    def test_gerar_qrcode_logo_inexistente(self):
        """Teste: comportamento com caminho de logo inexistente"""
        url = "https://example.com"
        result = gerar_qrcode(url, logo_path="/caminho/inexistente.png")

        # Deve gerar QR code normalmente, ignorando o logo
        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"  # Verificar modo em vez de format

    def test_gerar_qrcode_logo_vazio(self):
        """Teste: comportamento com logo_path vazio"""
        url = "https://example.com"
        result = gerar_qrcode(url, logo_path="")

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"  # Verificar modo em vez de format

    def test_gerar_qrcode_logo_apenas_espacos(self):
        """Teste: comportamento com logo_path contendo apenas espaços"""
        url = "https://example.com"
        result = gerar_qrcode(url, logo_path="   ")

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"  # Verificar modo em vez de format

    @pytest.mark.parametrize("url", [
        "https://google.com",
        "https://github.com",
        "https://python.org",
        "https://fastapi.tiangolo.com",
        "https://www.example-very-long-domain-name.com/path/to/resource?param=value",
        "mailto:test@example.com",
        "tel:+1234567890",
    ])
    def test_multiplas_urls_validas(self, url):
        """Teste: múltiplas URLs e tipos de dados válidos"""
        result = gerar_qrcode(url)

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"  # Verificar modo em vez de format
        assert result.size[0] > 0
        assert result.size[1] > 0

    def test_qrcode_tem_modo_rgba(self):
        """Teste: QR code gerado tem modo RGBA"""
        url = "https://example.com"
        result = gerar_qrcode(url)

        assert result.mode == "RGBA"

    def test_qrcode_com_caracteres_especiais(self):
        """Teste: QR code com caracteres especiais na URL"""
        url = "https://example.com/path?param=valor&outro=ação&emoji=🚀"
        result = gerar_qrcode(url)

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"  # Verificar modo em vez de format


class TestFuncoesUtilitarias:
    """Testes para funções utilitárias"""

    def test_arredondar_cantos(self):
        """Teste: função arredondar_cantos"""
        # Criar uma imagem teste
        img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))

        result = arredondar_cantos(img, raio=10)

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"
        assert result.size == img.size

    def test_arredondar_cantos_raio_zero(self):
        """Teste: arredondar cantos com raio zero"""
        img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))

        result = arredondar_cantos(img, raio=0)

        assert isinstance(result, Image.Image)
        assert result.size == img.size

    def test_arredondar_cantos_raio_grande(self):
        """Teste: arredondar cantos com raio muito grande"""
        img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))

        result = arredondar_cantos(img, raio=50)

        assert isinstance(result, Image.Image)
        assert result.size == img.size

    def test_criar_moldura_arredondada(self):
        """Teste: função criar_moldura_arredondada"""
        tamanho = (120, 120)
        cor = (255, 255, 255, 255)

        result = criar_moldura_arredondada(tamanho, raio=15, cor=cor)

        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"
        assert result.size == tamanho

    def test_criar_moldura_tamanhos_diferentes(self):
        """Teste: criar moldura com tamanhos diferentes"""
        tamanhos = [(50, 50), (100, 150), (200, 100)]

        for tamanho in tamanhos:
            result = criar_moldura_arredondada(tamanho, raio=10, cor=(0, 0, 0, 255))

            assert isinstance(result, Image.Image)
            assert result.size == tamanho
            assert result.mode == "RGBA"


class TestIntegracao:
    """Testes de integração"""

    def test_workflow_completo_sem_logo(self):
        """Teste: workflow completo de geração sem logo"""
        url = "https://integration-test.example.com"

        # Gerar QR code
        qr_image = gerar_qrcode(url)

        # Verificar resultado
        assert isinstance(qr_image, Image.Image)
        assert qr_image.mode == "RGBA"  # Verificar modo em vez de format
        assert qr_image.mode == "RGBA"

        # Salvar temporariamente para verificar se funciona
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            qr_image.save(temp_file.name, 'PNG')
            assert os.path.exists(temp_file.name)

            # Verificar se pode ser aberto novamente
            reloaded = Image.open(temp_file.name)
            assert reloaded.format == "PNG"

            # Cleanup
            os.unlink(temp_file.name)

    def test_workflow_completo_com_logo(self, sample_image):
        """Teste: workflow completo de geração com logo"""
        url = "https://integration-test-with-logo.example.com"

        # Gerar QR code com logo
        qr_image = gerar_qrcode(url, logo_path=sample_image)

        # Verificar resultado
        assert isinstance(qr_image, Image.Image)
        assert qr_image.mode == "RGBA"  # Verificar modo em vez de format
        assert qr_image.mode == "RGBA"

        # QR code com logo deve ser maior
        assert qr_image.size[0] > 200
        assert qr_image.size[1] > 200

        # Salvar e verificar
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            qr_image.save(temp_file.name, 'PNG')
            assert os.path.exists(temp_file.name)

            # Cleanup
            os.unlink(temp_file.name)
