from PIL import Image, ImageDraw
import qrcode

def arredondar_cantos(imagem, raio):
    mask = Image.new("L", imagem.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), imagem.size], radius=raio, fill=255)
    resultado = Image.new("RGBA", imagem.size)
    resultado.paste(imagem, (0, 0), mask=mask)
    return resultado

def criar_moldura_arredondada(tamanho_total, raio, cor):
    moldura = Image.new("RGBA", tamanho_total, (0, 0, 0, 0))
    draw = ImageDraw.Draw(moldura)
    draw.rounded_rectangle([(0, 0), (tamanho_total[0]-1, tamanho_total[1]-1)], radius=raio, fill=cor)
    return moldura

def gerar_qrcode(url, logo_path=None):
    data = url

    if not data:
        raise ValueError("Qrcode NÃO GERADO: Não foi passado uma URL para o Qrcode!!!")
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

        if logo_path and logo_path.strip():
            try:
                logo = Image.open(logo_path).convert("RGBA")
                
                logo_size = 100
                logo = logo.resize((logo_size, logo_size))

                raio_canto = 5
                logo_rounded = arredondar_cantos(logo, raio_canto)

                border_size = 5
                moldura_size = (logo_rounded.size[0] + 2*border_size, logo_rounded.size[1] + 2*border_size)
                moldura = criar_moldura_arredondada(moldura_size, raio_canto + border_size, cor=(255,255,255,255))

                pos_logo_na_moldura = (border_size, border_size)
                moldura.paste(logo_rounded, pos_logo_na_moldura, logo_rounded)

                pos = (
                    (qr_img.size[0] - moldura.size[0]) // 2,
                    (qr_img.size[1] - moldura.size[1]) // 2,
                )

                qr_img.paste(moldura, pos, moldura)

            except FileNotFoundError:
                raise FileNotFoundError("Logo não encontrada... Gerando Qrcode sem logo")

        return qr_img