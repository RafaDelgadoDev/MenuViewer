# 🔊 Text-to-Speech

**Status:** parcialmente implementado.

Os comandos de voz (`app/static/js/voz/`) já usam a Web Speech API (`SpeechSynthesisUtterance`) para ler em voz alta:

- “Ler descrição”: nome, preço, descrição e alérgenos do prato
- “Mostrar ingredientes”: a lista de ingredientes
- “Mostrar pratos”: os pratos na tela

Cada prato tem um botão Ouvir (`app/static/js/voz/ouvir.js`). Ele lê nome, preço, descrição e alérgenos com a mesma síntese, sem ligar o microfone. Um segundo clique interrompe a leitura.

## O que falta

- Opção de velocidade da fala
- Alternativa de áudio gerado no backend (ex.: gTTS) para vozes mais naturais ou navegadores sem síntese de voz

Quando essa parte for iniciada, crie uma issue vinculando este README.
