# Gerador de QrCode
Um Gerador de QrCode utilizando Python.

## Como Configurar no Debian/Ubuntu?
- Atualizar os pacotes: 
    ```
    sudo apt update
    ```
- Instalar as bibliotecas `pillow` e `qrcode`:
    > utilizando o apt:

    ```
    sudo apt install python3-pil python3-qrcode
    ```
    > utilizando o pip:

    ```
    pip install Pillow qrcode
    ```

## Como Configurar no Windows?
Com o Python instalado siga o passo abaixo utilizando o cmd ou PowerShell.
- Instalar as bibliotecas `pillow` e `qrcode`:

    ```
    pip install Pillow qrcode
    ```

## Como rodo o Programa?
- Abra um terminal na pasta onde está o arquivo `qrCode.py`
- rode o arquivo `qrCode.py`
- será solicitado `URL do Qrcode`
- passe uma URL, ex:
    ```
    https://google.com
    ```
    > OBS: em caso de não ser passado uma URL, será mostrado a mensagem `Qrcode NÃO GERADO: Não foi passado uma URL para o Qrcode!!!`
- Em seguida será solicitado o nome do arquivo da logo que deve estar em formato `.png` e na mesma pasta do arquivo `qrCode.py`.
    > Em caso do arquivo da logo não ser passado ou não existir, será criado um Qrcode sem logo.