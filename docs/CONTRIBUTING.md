# Como Contribuir para o Cardápio Digital Acessível

Primeiramente, muito obrigado pelo seu interesse em ajudar a tornar cardápios digitais mais acessíveis e inclusivos para todas as pessoas! 🎉

Todas as contribuições são bem-vindas: desde correção de *bugs*, melhorias na acessibilidade, novas funcionalidades até ajustes na documentação.

---

## 🚀 Fluxo de Desenvolvimento Local

### 1. Preparando o Ambiente
1. Faça um **Fork** deste repositório para o seu perfil.
2. Clone o seu fork localmente:
   ```bash
   git clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)
   cd NOME-DO-REPOSITORIO

```

3. Crie uma branch para as suas alterações:
```bash
git checkout -b feature/nome-da-sua-feature
# ou para correções de bug:
git checkout -b fix/descricao-do-bug

```



### 2. Configurando o Projeto

1. Instale as dependências de desenvolvimento:
```bash
pip install -r requirements-dev.txt
npm install

```


2. Execute a aplicação:
```bash
python run.py

```



---

## 🎨 Diretrizes do Projeto & Boas Práticas

Para manter a consistência do código e do produto, siga estas diretrizes essenciais:

### ♿ Acessibilidade em Primeiro Lugar (Core)

* **HTML Semântico**: Prefira sempre elementos nativos (`<button>`, `<a>`, `<details>`, `<dialog>`, `<label>`) antes de recorrer a atributos `aria-*`.
* **Navegação por Teclado**: Toda nova interface precisa ser 100% funcional via teclado com foco visível e sequencial (`Tab` / `Shift+Tab`).
* **Área de Toque**: Garanta o tamanho mínimo de **44×44px** em alvos clicáveis/tocáveis (`var(--alvo-min)`).
* **Contraste**: Respeite os padrões **WCAG AA** tanto no tema padrão quanto no modo de alto contraste. Utilize as variáveis de cor definidas em `style.css`.
* **Suporte a Zoom**: A interface deve continuar funcional com zoom de até 200% sem quebrar o layout ou ocultar informações.

### 🌐 Internacionalização (i18n)

* **Zero texto fixo (hardcoded) nos templates**: Qualquer texto exibido na interface deve ser adicionado nos arquivos de tradução em `app/translations/*.json` (português, inglês e espanhol) e invocado via `t('chave')`.

### 🏗️ Arquitetura & Código

* **Resiliência (Progressive Enhancement)**: Formulários e links devem funcionar **sem JavaScript**. O JS deve atuar apenas como uma camada de melhoria progressiva.
* **JavaScript Leve**: Utilize **JS Vanilla** com módulos ES. Não adicione frameworks ou bibliotecas pesadas. Mudanças nessa premissa devem ser discutidas previamente em uma *Issue*.
* **Regras de Negócio (Alérgenos)**: Alérgenos pertencem aos **ingredientes**, e não diretamente ao prato. Cadastre o ingrediente com os seus alérgenos correspondentes.
* **Banco de Dados**: Mudou o modelo? Sempre gere uma nova *migration*:
```bash
flask --app run db migrate -m "sua descrição sucinta aqui"

```


* **Commits**: Faça commits frequentes, pequenos e com mensagens claras e descritivas (ex: `fix: ajusta contraste do botão de busca`).

---

## 🧪 Testes e Validação

Antes de enviar sua contribuição, execute a suíte de testes locais:

```bash
# Testes do backend (Python)
pytest

# Testes do frontend (JavaScript)
npm test

```

### 📋 Checklist Manual de Acessibilidade

Como nem tudo é capturado por testes automatizados, realize a validação manual no navegador:

* [ ] **Teclado**: A página pode ser totalmente navegada usando apenas `Tab` / `Shift+Tab`? A ordem faz sentido e o foco está visível em todos os momentos?
* [ ] **Modais e Mídia**: Ao abrir e fechar a foto ampliada com `Enter` e `Esc`, o foco retorna para o botão que originou a ação?
* [ ] **Escala e Zoom**: Testou a página com **200% de zoom** no navegador e com a fonte configurada em 200% no painel?
* [ ] **Leitor de Tela**: Testou com NVDA, VoiceOver ou TalkBack? O leitor anuncia cada prato corretamente com nome, preço, descrição e alérgenos?
* [ ] **Modos de Exibição**: O funcionamento e a legibilidade continuam adequados no **alto contraste** e no **modo simplificado**?

---

## 📥 Enviando o Pull Request (PR)

Ao abrir seu Pull Request, certifique-se de:

1. **Descrição detalhada**: Explique o que foi alterado e o motivo da mudança.
2. **Contexto de Acessibilidade**: Se for uma melhoria de acessibilidade, mencione qual barreira ou necessidade de usuário ela resolve.
3. **Imagens/Vídeos**: Anexe *screenshots* ou gravações de tela, demonstrando principalmente o comportamento com alto contraste, fontes ampliadas ou modo simplificado.
4. **Vincular Issues**: Se o seu PR resolve uma issue existente, adicione na descrição: `Fixes #numero_da_issue`.

---

## 💡 O que desenvolver?

Está buscando ideias sobre onde começar a contribuir?

* Confira as [Issues abertas](https://www.google.com/search?q=../../issues) para encontrar tarefas já catalogadas.
* Veja a seção **"Ideias para o futuro"** no nosso [README](https://www.google.com/search?q=../README.md).
* Encontrou um bug ou tem uma sugestão? Sinta-se à vontade para [abrir uma nova Issue](https://www.google.com/search?q=../../issues/new).

```

---

### Principais melhorias aplicadas:
1. **Estrutura Visual Refinada**: Adoção de divisores e marcadores que facilitam a leitura rápida (*scannability*).
2. **Separação de Contextos**: Regras de Acessibilidade, Internacionalização e Arquitetura foram separadas em tópicos claros.
3. **Detalhamento do Git**: Adicionados comandos de `git clone` e padronização do nome de branches (`feature/` e `fix/`).
4. **Boas Práticas de PR**: Adicionada a instrução para vincular PRs a issues (`Fixes #123`), facilitando a gestão do repositório.

```
