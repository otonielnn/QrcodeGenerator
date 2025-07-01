from PIL import Image, ImageDraw
import qrcode
import os
from sys import platform

def arredondar_cantos(imagem, raio):
    mask = Image.new("L", imagem.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), imagem.size], radius=raio, fill=255)
    resultado = Image.new("RGBA", imagem.size)
    resultado.paste(imagem, (0, 0), mask=mask)
    return resultado

def criar_moldura_arredondada(tamanho_total, raio, cor):
    # Cria uma imagem transparente
    moldura = Image.new("RGBA", tamanho_total, (0, 0, 0, 0))
    draw = ImageDraw.Draw(moldura)
    # Desenha um retângulo arredondado preenchido com a cor passada (ex: branco)
    draw.rounded_rectangle([(0, 0), (tamanho_total[0]-1, tamanho_total[1]-1)], radius=raio, fill=cor)
    return moldura

# Dados do QR
data = input("URL do qrCode: ")

if data == "":
    print("Qrcode NÃO GERADO: Não foi passado uma URL para o Qrcode!!!")
else:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Abrir logo
    logo_img = input("Digite o nome do arquivo da logo (precisa está em formato png): ")
    if logo_img == "":
        pass
    else:
        try:
            logo = Image.open(logo_img).convert("RGBA")
            # Redimensionar logo
            logo_size = 100
            logo = logo.resize((logo_size, logo_size))

            # Arredondar cantos da logo
            raio_canto = 5
            logo_rounded = arredondar_cantos(logo, raio_canto)

            # Criar moldura (borda branca) maior que a logo arredondada
            border_size = 5
            moldura_size = (logo_rounded.size[0] + 2*border_size, logo_rounded.size[1] + 2*border_size)
            moldura = criar_moldura_arredondada(moldura_size, raio_canto + border_size, cor=(255,255,255,255))

            # Colar logo arredondada no centro da moldura
            pos_logo_na_moldura = (border_size, border_size)
            moldura.paste(logo_rounded, pos_logo_na_moldura, logo_rounded)

            # Posicionar moldura+logo no centro do QR Code
            pos = (
                (qr_img.size[0] - moldura.size[0]) // 2,
                (qr_img.size[1] - moldura.size[1]) // 2,
            )

            # Colar moldura (com logo) no QR Code usando máscara para preservar transparência
            qr_img.paste(moldura, pos, moldura)

        except FileNotFoundError:
            print("Logo não encontrada... Gerando Qrcode sem logo")

    # Salvar e abrir
    qr_img.save("qrcode.png")
    if platform == "linux":
        os.system("open qrcode.png")
    elif platform == "win32":
        os.startfile("qrcode.png")