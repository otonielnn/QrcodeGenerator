"""
Testes para os endpoints da API FastAPI
"""
import io

import pytest
from PIL import Image


class TestQRCodeEndpoint:
    """Testes para o endpoint /gerar-qrcode"""

    def test_gerar_qrcode_simples(self, client):
        """Teste básico: gerar QR code apenas com URL"""
        response = client.post(
            "/gerar-qrcode",
            data={"url": "https://google.com"}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert "qrcode.png" in response.headers.get("content-disposition", "")

        # Verificar se é uma imagem PNG válida
        img = Image.open(io.BytesIO(response.content))
        assert img.format == "PNG"
        assert img.size[0] > 0
        assert img.size[1] > 0

    def test_gerar_qrcode_com_filename_customizado(self, client):
        """Teste: gerar QR code com nome de arquivo personalizado"""
        filename = "meu_qrcode_teste.png"
        response = client.post(
            "/gerar-qrcode",
            data={
                "url": "https://example.com",
                "filename": filename
            }
        )

        assert response.status_code == 200
        assert filename in response.headers.get("content-disposition", "")

    def test_gerar_qrcode_com_logo(self, client, sample_logo_file):
        """Teste: gerar QR code com logo"""
        with open(sample_logo_file, "rb") as logo_file:
            response = client.post(
                "/gerar-qrcode",
                data={"url": "https://github.com"},
                files={"logo": ("logo.png", logo_file, "image/png")}
            )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

        # Verificar se a imagem foi gerada corretamente
        img = Image.open(io.BytesIO(response.content))
        assert img.format == "PNG"

    def test_gerar_qrcode_com_logo_e_filename(self, client, sample_logo_file):
        """Teste: gerar QR code com logo e filename personalizado"""
        filename = "qr_com_logo.png"

        with open(sample_logo_file, "rb") as logo_file:
            response = client.post(
                "/gerar-qrcode",
                data={
                    "url": "https://python.org",
                    "filename": filename
                },
                files={"logo": ("logo.png", logo_file, "image/png")}
            )

        assert response.status_code == 200
        assert filename in response.headers.get("content-disposition", "")
    
    def test_gerar_qrcode_url_vazia(self, client):
        """Teste: erro quando URL está vazia"""
        response = client.post(
            "/gerar-qrcode",
            data={"url": ""}
        )
        
        # FastAPI pode retornar 422 para campo vazio ou 400 para validação
        assert response.status_code in {400, 422}

    def test_gerar_qrcode_sem_url(self, client):
        """Teste: erro quando URL não é fornecida"""
        response = client.post(
            "/gerar-qrcode",
            data={}
        )

        assert response.status_code == 422  # Unprocessable Entity

    def test_gerar_qrcode_apenas_espacos(self, client):
        """Teste: erro quando URL contém apenas espaços"""
        response = client.post(
            "/gerar-qrcode",
            data={"url": "   "}
        )

        assert response.status_code == 400

    @pytest.mark.parametrize("url", [
        "https://google.com",
        "https://github.com",
        "https://example.com",
        "https://python.org",
        "https://fastapi.tiangolo.com",
    ])
    def test_multiplas_urls_validas(self, client, url):
        """Teste: múltiplas URLs válidas"""
        response = client.post(
            "/gerar-qrcode",
            data={"url": url}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_logo_arquivo_invalido(self, client, invalid_image_file):
        """Teste: comportamento com arquivo de logo inválido"""
        with open(invalid_image_file, "rb") as invalid_file:
            response = client.post(
                "/gerar-qrcode",
                data={"url": "https://example.com"},
                files={"logo": ("invalid.txt", invalid_file, "text/plain")}
            )

        # Deve ainda gerar QR code, mas sem logo
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_logo_vazio(self, client):
        """Teste: arquivo de logo vazio"""
        response = client.post(
            "/gerar-qrcode",
            data={"url": "https://example.com"},
            files={"logo": ("", b"", "image/png")}
        )

        # Deve gerar QR code sem logo
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_content_type_correto(self, client):
        """Teste: verifica se o Content-Type está correto"""
        response = client.post(
            "/gerar-qrcode",
            data={"url": "https://example.com"}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_content_disposition_header(self, client):
        """Teste: verifica se o header Content-Disposition está presente"""
        response = client.post(
            "/gerar-qrcode",
            data={
                "url": "https://example.com",
                "filename": "teste.png"
            }
        )

        assert response.status_code == 200
        content_disposition = response.headers.get("content-disposition")
        assert content_disposition is not None
        assert "attachment" in content_disposition
        assert "teste.png" in content_disposition

    def test_tamanho_resposta_razoavel(self, client):
        """Teste: verifica se o tamanho da resposta é razoável"""
        response = client.post(
            "/gerar-qrcode",
            data={"url": "https://example.com"}
        )

        assert response.status_code == 200

        # QR code não deve ser muito pequeno nem muito grande
        content_length = len(response.content)
        assert content_length > 1000  # Pelo menos 1KB
        assert content_length < 1000000  # Não mais que 1MB
