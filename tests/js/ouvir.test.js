import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { montarTextoOuvir } from "../../app/static/js/voz/ouvir.js";

describe("montarTextoOuvir", () => {
    it("junta nome, preço, descrição e alérgenos", () => {
        assert.equal(
            montarTextoOuvir({
                nome: "Risoto de Funghi",
                preco: "R$ 48,00",
                descricao: "Arroz arbóreo com cogumelos.",
                alergenos: "Contém: leite.",
            }),
            "Risoto de Funghi, R$ 48,00. Arroz arbóreo com cogumelos. Contém: leite.",
        );
    });

    it("omite partes vazias e junta espaços repetidos", () => {
        assert.equal(
            montarTextoOuvir({ nome: "Suco", preco: "R$ 8,00", descricao: "  ", alergenos: "" }),
            "Suco, R$ 8,00.",
        );
        assert.equal(
            montarTextoOuvir({ nome: "Água", preco: "", descricao: "Sem gás.", alergenos: "  Sem   alérgenos.  " }),
            "Água. Sem gás. Sem alérgenos.",
        );
    });
});
