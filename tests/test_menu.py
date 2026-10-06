from decimal import Decimal

from tests.conftest import nomes_dos_pratos


def test_pagina_carrega_com_todas_as_categorias(pagina):
    soup = pagina("/")
    assert soup.h1.get_text(strip=True) == "Nosso cardápio"
    categorias = [h.get_text(strip=True) for h in soup.select("section.categoria h2")]
    assert categorias == ["Entradas", "Pratos Principais", "Sobremesas", "Bebidas"]
    assert len(nomes_dos_pratos(soup)) == 9


def test_preco_formatado_em_reais(pagina):
    soup = pagina("/")
    preco = soup.select_one("#prato-1 .prato-preco data")
    assert preco["value"] == "22.00"
    assert preco.get_text(strip=True) == "R$ 22,00"


def test_alergenos_derivados_dos_ingredientes(pagina):
    soup = pagina("/")
    petit = next(a for a in soup.select("article.prato") if "Petit Gateau" in a.h3.text)
    texto = petit.select_one("[data-alergenos]").get_text(" ", strip=True)
    for alergeno in ("glúten", "leite", "ovo", "soja"):
        assert alergeno in texto


def test_propriedades_derivadas_do_modelo(app):
    from app.extensions import db
    from app.models import Prato

    curry = db.session.execute(
        db.select(Prato).filter_by(nome="Curry Picante de Grão-de-bico")
    ).scalar_one()
    risoto = db.session.execute(
        db.select(Prato).filter_by(nome="Risoto de Funghi")
    ).scalar_one()
    camarao = db.session.execute(
        db.select(Prato).filter_by(nome="Camarão ao Alho")
    ).scalar_one()

    assert curry.vegano and curry.vegetariano and curry.alergenos == []
    assert not risoto.vegano and risoto.vegetariano
    assert [a.codigo for a in risoto.alergenos] == ["leite"]
    assert not camarao.vegetariano
    assert isinstance(curry.preco, Decimal)


def test_link_para_qrcode_no_rodape(pagina):
    soup = pagina("/")
    assert soup.select_one("footer a[href='/qrcode']")


def test_api_cardapio_retorna_json_com_categorias_e_pratos(app):
    cliente = app.test_client()

    resposta = cliente.get("/api/cardapio")

    assert resposta.status_code == 200
    assert resposta.is_json

    dados = resposta.get_json()

    assert "categorias" in dados
    assert "total_pratos" in dados
    assert "filtros" in dados

    assert dados["total_pratos"] == 9
    assert [categoria["nome"] for categoria in dados["categorias"]] == [
        "Entradas",
        "Pratos Principais",
        "Sobremesas",
        "Bebidas",
    ]


def test_api_cardapio_retorna_dados_completos_do_prato(app):
    cliente = app.test_client()

    resposta = cliente.get("/api/cardapio")

    dados = resposta.get_json()

    entradas = dados["categorias"][0]
    petit = next(
        prato
        for prato in dados["categorias"][2]["pratos"]
        if prato["nome"] == "Petit Gateau"
    )

    assert entradas["id"] == 1
    assert entradas["ordem"] == 1

    assert petit["descricao"]
    assert petit["preco"] == 28.0
    assert petit["picante"] is False
    assert petit["disponivel"] is True
    assert petit["vegano"] is False
    assert petit["vegetariano"] is True
    assert "leite" in petit["alergenos"]
    assert "ovo" in petit["alergenos"]
    assert len(petit["ingredientes"]) > 0


def test_api_cardapio_respeita_filtros(app):
    cliente = app.test_client()

    resposta = cliente.get("/api/cardapio?dieta=vegano")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    nomes = [
        prato["nome"]
        for categoria in dados["categorias"]
        for prato in categoria["pratos"]
    ]

    assert dados["filtros"]["dietas"] == ["vegano"]
    assert nomes
    assert "Curry Picante de Grão-de-bico" in nomes
    assert "Petit Gateau" not in nomes