import io

import segno
import pytest


def test_pagina_do_qrcode(pagina):
    soup = pagina("/qrcode")
    img = soup.select_one(".cartao-qrcode img")
    assert img["src"] == "/qrcode.svg"
    assert "http://localhost/" in img["alt"]
    assert soup.select_one(".cartao-url").get_text(strip=True) == "http://localhost/"


def test_svg_codifica_a_url_do_cardapio(client):
    resposta = client.get("/qrcode.svg")
    assert resposta.mimetype == "image/svg+xml"
    esperado = io.BytesIO()
    segno.make("http://localhost/", error="m").save(
        esperado, kind="svg", scale=10, border=4, xmldecl=False,
        title="QR Code do cardápio", svgclass=None, lineclass=None,
    )
    assert resposta.data == esperado.getvalue()


def test_png_para_download(client):
    resposta = client.get("/qrcode.png?download=1")
    assert resposta.mimetype == "image/png"
    assert resposta.data.startswith(b"\x89PNG")
    assert "attachment" in resposta.headers["Content-Disposition"]


def test_usa_url_publica_configurada(app, client):
    app.config["PUBLIC_BASE_URL"] = "https://cardapio.exemplo.com.br/"
    soup_texto = client.get("/qrcode").get_data(as_text=True)
    assert "https://cardapio.exemplo.com.br/" in soup_texto


def test_formato_invalido(client):
    assert client.get("/qrcode.gif").status_code == 404


@pytest.mark.parametrize("idioma,titulo", [
    ("pt", "QR Code do cardápio"),
    ("en", "Menu QR code"),
    ("es", "Código QR del menú"),
])
def test_titulo_svg_acompanha_idioma(client, idioma, titulo):
    from xml.etree import ElementTree

    resposta = client.get("/qrcode.svg", headers={"Accept-Language": idioma})
    svg = ElementTree.fromstring(resposta.data)
    assert svg.find("{http://www.w3.org/2000/svg}title").text == titulo
    assert "Accept-Language" in resposta.vary
    assert "Cookie" in resposta.vary


def test_titulo_svg_respeita_idioma_do_cookie(client, definir_prefs):
    definir_prefs(idioma="es")
    resposta = client.get("/qrcode.svg", headers={"Accept-Language": "en"})
    assert "Código QR del menú" in resposta.get_data(as_text=True)
