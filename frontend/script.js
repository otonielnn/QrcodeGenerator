function getApiUrl() {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    
    if (hostname !== 'localhost' && hostname !== '127.0.0.1' && hostname !== '') {
        if (window.location.port === '' || window.location.port === '80' || window.location.port === '443') {
            return `${protocol}//${hostname}/gerar-qrcode`;
        }
        return `${protocol}//${hostname}:8000/gerar-qrcode`;
    } else {
        return 'http://localhost:8000/gerar-qrcode';
    }
}

const API_URL = getApiUrl();

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
        alert('Erro ao gerar QR Code. Verifique se a API está rodando na porta 8000.');
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
