function getApiUrl() {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    
    // Se estiver em desenvolvimento local
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '') {
        return 'http://localhost:8000/gerar-qrcode';
    }
    
    // Se estiver em produção (Render ou qualquer outro host)
    // A API está no mesmo domínio, apenas usa o path
    return `${protocol}//${hostname}/gerar-qrcode`;
}

const API_URL = getApiUrl();

// Log para debug
console.log('API URL configurada:', API_URL);
console.log('Hostname atual:', window.location.hostname);
console.log('Protocol atual:', window.location.protocol);

// Event listener para preview da imagem
document.getElementById('logo').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const previewContainer = document.getElementById('logo-preview');
    const previewImage = document.getElementById('preview-image');
    const fileName = document.getElementById('file-name');
    
    if (file) {
        // Verificar se é uma imagem
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                fileName.textContent = `Arquivo: ${file.name}`;
                previewContainer.classList.remove('logo-preview-hidden');
            };
            reader.readAsDataURL(file);
        } else {
            alert('Por favor, selecione apenas arquivos de imagem!');
            event.target.value = '';
        }
    } else {
        previewContainer.classList.add('logo-preview-hidden');
    }
});

// Event listener para remover logo
document.getElementById('remove-logo').addEventListener('click', function() {
    document.getElementById('logo').value = '';
    document.getElementById('logo-preview').classList.add('logo-preview-hidden');
});

document.getElementById('gerar-btn').addEventListener('click', async function () {
    const urlInput = document.getElementById('url').value;
    const logoFile = document.getElementById('logo').files[0];

    if (!urlInput.trim()) {
        alert('Por favor, digite uma URL válida!');
        return;
    }

    mostrarLoading();
    esconderContainer();

    try {
        const formData = new FormData();
        formData.append('url', urlInput);
        formData.append('filename', 'qrcode.png');

        if (logoFile) {
            formData.append('logo', logoFile);
        }

        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }

        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);

        exibirQRCode(imageUrl);

    } catch (error) {
        console.error('Erro ao gerar QR Code:', error);
        console.error('API URL:', API_URL);
        
        let errorMessage = 'Erro ao gerar QR Code.';
        
        if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Erro de conexão com a API. Verifique sua conexão com a internet.';
        } else if (error.message.includes('404')) {
            errorMessage = 'Endpoint da API não encontrado. Verifique se a API está configurada corretamente.';
        } else if (error.message.includes('405')) {
            errorMessage = 'Método não permitido. Problema na configuração da API.';
        } else if (error.message.includes('500')) {
            errorMessage = 'Erro interno do servidor. Tente novamente em alguns minutos.';
        }
        
        alert(`${errorMessage}\n\nDetalhes técnicos: ${error.message}\nAPI URL: ${API_URL}`);
    } finally {
        esconderLoading();
    }
});

function mostrarLoading() {
    document.getElementById('loading').style.display = 'block';
}

function esconderLoading() {
    document.getElementById('loading').style.display = 'none';
}

function exibirQRCode(imageUrl) {
    const qrcodeImage = document.getElementById('qrcode-image');
    const qrcodeContainer = document.getElementById('qrcode-container');
    const downloadBtn = document.getElementById('download-btn');

    qrcodeImage.src = imageUrl;

    qrcodeContainer.style.display = 'block';

    downloadBtn.onclick = function () {
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = 'qrcode.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };
}

function esconderContainer() {
    document.getElementById('qrcode-container').style.display = 'none';
}
