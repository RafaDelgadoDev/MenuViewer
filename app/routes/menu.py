from flask import Blueprint, g, jsonify, render_template, request

from app.services.cardapio import (
    DIETAS,
    FiltroCardapio,
    buscar_categorias,
    contar_pratos,
    listar_alergenos,
)

menu_bp = Blueprint("menu", __name__)


@menu_bp.route("/")
def index():
    alergenos = listar_alergenos()
    filtro = FiltroCardapio.from_args(request.args, {a.codigo for a in alergenos})
    categorias = buscar_categorias(filtro)

    contexto = {
        "categorias": categorias,
        "total_pratos": contar_pratos(categorias),
        "filtro": filtro,
        "dietas": DIETAS,
        "alergenos": alergenos,
    }

    if g.prefs.simplificado:
        return render_template(
            "menu_simplificado.html",
            **contexto,
            **_passo_atual(categorias),
        )

    return render_template("menu.html", **contexto)


@menu_bp.route("/api/cardapio")
def api_cardapio():
    """Retorna o cardápio disponível em formato JSON."""

    alergenos = listar_alergenos()
    filtro = FiltroCardapio.from_args(
        request.args,
        {a.codigo for a in alergenos},
    )
    categorias = buscar_categorias(filtro)

    dados = {
        "categorias": [
            {
                "id": categoria.id,
                "nome": categoria.nome,
                "ordem": categoria.ordem,
                "pratos": [
                    {
                        "id": prato.id,
                        "nome": prato.nome,
                        "descricao": prato.descricao,
                        "preco": float(prato.preco),
                        "imagem": prato.imagem,
                        "imagem_alt": prato.imagem_alt,
                        "picante": prato.picante,
                        "disponivel": prato.disponivel,
                        "ordem": prato.ordem,
                        "vegano": prato.vegano,
                        "vegetariano": prato.vegetariano,
                        "ingredientes": [
                            ingrediente.nome
                            for ingrediente in prato.ingredientes
                        ],
                        "alergenos": [
                            alergeno.codigo
                            for alergeno in prato.alergenos
                        ],
                    }
                    for prato in categoria.pratos
                ],
            }
            for categoria in categorias
        ],
        "total_pratos": contar_pratos(categorias),
        "filtros": {
            "dietas": sorted(filtro.dietas),
            "sem": sorted(filtro.excluir_alergenos),
        },
    }

    return jsonify(dados)


def _passo_atual(categorias):
    """No modo simplificado, qual categoria mostrar e quais são as vizinhas."""
    if not categorias:
        return {"atual": None, "indice": 0, "anterior": None, "proxima": None}

    categoria_id = request.args.get("categoria", type=int)
    indice = next(
        (i for i, c in enumerate(categorias) if c.id == categoria_id),
        0,
    )

    return {
        "atual": categorias[indice],
        "indice": indice,
        "anterior": categorias[indice - 1] if indice > 0 else None,
        "proxima": (
            categorias[indice + 1]
            if indice + 1 < len(categorias)
            else None
        ),
    }