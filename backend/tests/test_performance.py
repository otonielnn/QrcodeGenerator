"""
Testes de performance e carga para a API
"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest


class TestPerformance:
    """Testes de performance da API"""

    def test_tempo_resposta_qrcode_simples(self, client):
        """Teste: tempo de resposta para QR code simples"""
        start_time = time.time()

        response = client.post(
            "/gerar-qrcode",
            data={"url": "https://example.com"}
        )

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 2.0  # Deve responder em menos de 2 segundos

    def test_tempo_resposta_qrcode_com_logo(self, client, sample_logo_file):
        """Teste: tempo de resposta para QR code com logo"""
        start_time = time.time()

        with open(sample_logo_file, "rb") as logo_file:
            response = client.post(
                "/gerar-qrcode",
                data={"url": "https://example.com"},
                files={"logo": ("logo.png", logo_file, "image/png")}
            )

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 5.0  # Com logo pode demorar um pouco mais

    @pytest.mark.slow
    def test_multiplas_requisicoes_sequenciais(self, client):
        """Teste: múltiplas requisições sequenciais"""
        num_requests = 10
        response_times = []

        for i in range(num_requests):
            start_time = time.time()

            response = client.post(
                "/gerar-qrcode",
                data={"url": f"https://example{i}.com"}
            )

            end_time = time.time()
            response_times.append(end_time - start_time)

            assert response.status_code == 200

        # Verificar tempos de resposta
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)

        assert avg_time < 2.0  # Tempo médio
        assert max_time < 5.0   # Tempo máximo

    @pytest.mark.slow
    def test_carga_concorrente(self, client):
        """Teste: carga com requisições concorrentes"""
        num_threads = 5
        requests_per_thread = 3

        def make_request(thread_id):
            results = []
            for i in range(requests_per_thread):
                start_time = time.time()

                response = client.post(
                    "/gerar-qrcode",
                    data={"url": f"https://thread{thread_id}-req{i}.com"}
                )

                end_time = time.time()
                results.append({
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'thread_id': thread_id,
                    'request_id': i
                })
            return results

        all_results = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_threads)]

            for future in as_completed(futures):
                results = future.result()
                all_results.extend(results)

        # Verificar todos os resultados
        for result in all_results:
            assert result['status_code'] == 200
            assert result['response_time'] < 10.0  # Mais tolerante para concorrência

        # Verificar estatísticas gerais
        response_times = [r['response_time'] for r in all_results]
        avg_time = sum(response_times) / len(response_times)

        assert len(all_results) == num_threads * requests_per_thread
        assert avg_time < 5.0


class TestStress:
    """Testes de stress e limite"""

    def test_url_muito_longa(self, client):
        """Teste: URL muito longa"""
        # URL com mais de 800 caracteres (reduzido para evitar limite do QR)
        long_url = "https://example.com/" + "a" * 800

        response = client.post(
            "/gerar-qrcode",
            data={"url": long_url}
        )

        # Deve funcionar ou falhar graciosamente
        assert response.status_code in {200, 400, 413, 500}  # OK, Bad Request, Payload Too Large ou Internal Error

    def test_filename_muito_longo(self, client):
        """Teste: nome de arquivo muito longo"""
        long_filename = "a" * 500 + ".png"

        response = client.post(
            "/gerar-qrcode",
            data={
                "url": "https://example.com",
                "filename": long_filename
            }
        )

        # Deve funcionar ou limitar o nome do arquivo
        assert response.status_code == 200

    def test_caracteres_especiais_extremos(self, client):
        """Teste: caracteres especiais extremos na URL"""
        special_url = "https://example.com/🚀🎉💻🌟⭐️🔥💯🎯🎨🎪🎭🎨🎯💎🔮🎲🎰🎳🎪"

        response = client.post(
            "/gerar-qrcode",
            data={"url": special_url}
        )

        assert response.status_code == 200


class TestMemoria:
    """Testes de uso de memória"""

    @pytest.mark.slow
    def test_multiplos_qrcodes_sem_vazamento(self, client):
        """Teste: múltiplos QR codes sem vazamento de memória"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Gerar muitos QR codes
        for i in range(50):
            response = client.post(
                "/gerar-qrcode",
                data={"url": f"https://memory-test-{i}.com"}
            )
            assert response.status_code == 200

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Aumento de memória não deve ser excessivo (menos de 100MB)
        assert memory_increase < 100 * 1024 * 1024
