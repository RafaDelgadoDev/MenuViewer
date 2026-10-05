// Botão "Ouvir" de cada prato. Não depende do microfone: só da síntese de voz
// do navegador. Quem usa comando de voz continua com "ler descrição".
import { anunciar } from "../anuncios.js";

/** Junta as partes visíveis do prato na mesma ordem da leitura por voz. */
export function montarTextoOuvir({ nome = "", preco = "", descricao = "", alergenos = "" } = {}) {
    const limpar = (texto) => String(texto).replace(/\s+/g, " ").trim();
    const cabeca = [limpar(nome), limpar(preco)].filter(Boolean).join(", ");
    return [cabeca ? `${cabeca}.` : "", limpar(descricao), limpar(alergenos)].filter(Boolean).join(" ");
}

export function textoDoPrato(el) {
    return montarTextoOuvir({
        nome: el.dataset.nome,
        preco: el.querySelector(".prato-preco data")?.textContent ?? "",
        descricao: el.querySelector("[data-descricao]")?.textContent ?? "",
        alergenos: el.querySelector("[data-alergenos]")?.textContent ?? "",
    });
}

/**
 * Mostra os botões se o navegador souber falar e liga o clique.
 * `controle` é opcional: quando os comandos de voz estão ligados, ele pausa
 * o microfone enquanto o prato é lido, para o app não ouvir a própria fala.
 */
export function ligarBotoesOuvir(controle) {
    const sintese = window.speechSynthesis;
    if (!sintese || !window.SpeechSynthesisUtterance) return;

    let botaoAtivo = null;

    const soltar = (botao) => {
        if (botaoAtivo === botao) botaoAtivo = null;
        botao.setAttribute("aria-pressed", "false");
    };

    document.querySelectorAll("[data-ouvir]").forEach((botao) => {
        botao.hidden = false;
        botao.addEventListener("click", () => {
            const prato = botao.closest("[data-prato]");
            if (!prato) return;

            if (botaoAtivo === botao) {
                sintese.cancel();
                soltar(botao);
                controle?.retomarDepoisDeFalaExterna();
                return;
            }

            const texto = textoDoPrato(prato);
            if (!texto) return;

            sintese.cancel();
            if (botaoAtivo) soltar(botaoAtivo);
            controle?.pausarParaFalaExterna();

            botaoAtivo = botao;
            botao.setAttribute("aria-pressed", "true");
            anunciar(texto);

            const fala = new SpeechSynthesisUtterance(texto);
            fala.lang = document.documentElement.lang || "pt-BR";
            const fim = () => {
                // Outro clique já assumiu a fala: não religa o microfone no meio dela.
                if (botaoAtivo !== botao) return;
                soltar(botao);
                controle?.retomarDepoisDeFalaExterna();
            };
            fala.onend = fim;
            fala.onerror = fim;
            sintese.speak(fala);
        });
    });
}
