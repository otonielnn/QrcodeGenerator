from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import uvicorn
from typing import Optional

try:
    from backend.qrcode_utils import gerar_qrcode
except ImportError:
    from qrcode_utils import gerar_qrcode

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/gerar-qrcode")
def gerar_qrcode_endpoint(
    url: str = Form(...),
    filename: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None)
):
    if not url:
        raise HTTPException(status_code=400, detail="URL do QR Code não fornecida.")
    
    logo_path = None
    
    if logo and logo.filename:
        try:
            import tempfile
            import os
            
            temp_dir = tempfile.mkdtemp()
            logo_path = os.path.join(temp_dir, logo.filename)
            
            with open(logo_path, "wb") as buffer:
                content = logo.file.read()
                buffer.write(content)
                
        except Exception as e:
            print(f"Erro ao processar logo: {e}")
            logo_path = None
    
    qr_image = gerar_qrcode(url, logo_path=logo_path)
    
    if logo_path and os.path.exists(logo_path):
        try:
            os.remove(logo_path)
            os.rmdir(os.path.dirname(logo_path))
        except Exception:
            pass

    img_io = io.BytesIO()
    qr_image.save(img_io, format='PNG')
    img_io.seek(0)

    return StreamingResponse(
        img_io,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename={filename or 'qrcode.png'}"}
    )

if __name__ == "__main__":
    import sys
    import os
    import socket
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "localhost"
    
    local_ip = get_local_ip()
    
    print("🚀 Iniciando API do QR Code Generator...")
    print("📡 API disponível em:")
    print("   • Local: http://localhost:8000")
    print(f"   • Rede Local: http://{local_ip}:8000")
    print("📚 Documentação em:")
    print("   • Local: http://localhost:8000/docs")
    print(f"   • Rede Local: http://{local_ip}:8000/docs")
    print("🛑 Para parar: Ctrl+C")
    print("-" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )