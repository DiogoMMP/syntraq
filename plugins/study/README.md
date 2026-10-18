# `study` — Estudo

Parte do [Syntraq](../../README.md) — *Power up your agents*.

Skills de estudo que trabalham por cima de uma knowledge base em modo research (criada pelo [`knowledge-base`](../knowledge-base/README.md)): leem o que está em `raw/` — slides, livros, fichas, exames antigos, sem impor nenhuma estrutura — e na `wiki/`, escrevem o conhecimento na wiki e o material de estudo em `outputs/<cadeira>/estudo/`.

## Como se ligam

1. **`exam-map`** lê os exames antigos e escreve na wiki o que sai, com que peso, e um catálogo de perguntas reais — a base de tudo o resto.
2. **`study-summary`**, **`flashcards`** e **`quiz`** dão a matéria com mais espaço ao que mais sai.
3. **`mock-exam`** e **`solve-exam`** treinam o exame: simulados no formato real e resoluções só com a matéria da cadeira.
4. **`correct-attempt`** corrige as tuas tentativas e mantém o registo de pontos fracos, que o `quiz`, o `mock-exam`, o `study-summary` e o `study-plan` usam.
5. **`study-plan`** junta tudo num calendário até aos exames.

## Instalação

```text
/plugin marketplace add DiogoMMP/syntraq
/plugin install study@syntraq
```

O material para imprimir (resumos, simulados, resoluções) é gerado em Word e PDF com o [pandoc](https://pandoc.org) e o Microsoft Word (ou o LibreOffice) — as skills perguntam antes de instalar o pandoc. Os flashcards exportam para o ficheiro de texto do Anki sem instalar nada, ou para `.apkg` com o `genanki`.

## Skills

| Skill | O que faz |
| :--- | :--- |
| [`exam-map`](skills/exam-map/SKILL.md) | Mapeia o que sai nos exames de uma cadeira |
| [`study-summary`](skills/study-summary/SKILL.md) | Escreve um resumo completo para imprimir, em Word e PDF |
| [`mock-exam`](skills/mock-exam/SKILL.md) | Cria simulados de exame com enunciado e correção separados |
| [`solve-exam`](skills/solve-exam/SKILL.md) | Resolve exames e fichas só com a matéria da cadeira |
| [`correct-attempt`](skills/correct-attempt/SKILL.md) | Corrige as tuas tentativas e regista os pontos fracos |
| [`quiz`](skills/quiz/SKILL.md) | Tutor no chat que te faz perguntas, focado nos pontos fracos |
| [`flashcards`](skills/flashcards/SKILL.md) | Cria flashcards para o Anki |
| [`study-plan`](skills/study-plan/SKILL.md) | Faz o plano de estudo, dia a dia, até aos exames |

## Em detalhe

<details>
<summary><b><code>exam-map</code></b> — Mapeia o que sai nos exames de uma cadeira</summary>

Descobre os exames antigos em `raw/` pelo caminho, nome e conteúdo (exames, exame modelo, testes e resoluções), mostra a lista para confirmares na primeira vez, lê-os (com OCR quando são digitalizados) e classifica cada pergunta pelos artigos da própria wiki. Escreve na `wiki/` um artigo de exames — formato, tabela tema × exame com o peso de cada tema, ranking 🔥/⚠️/📎, tendências, tipos de pergunta, perguntas repetidas, estilo do professor e prioridades de estudo marcadas como interpretação — e um catálogo de perguntas com ids estáveis, de onde as outras skills de estudo tiram perguntas reais. Atualiza o artigo de avaliação que já exista em vez de criar outro, regista os exames em `wiki/sources.md`, é incremental (só lê exames novos) e assinala análises repetidas em `outputs/`.

→ [`SKILL.md`](skills/exam-map/SKILL.md)

</details>

<details>
<summary><b><code>study-summary</code></b> — Escreve um resumo completo para imprimir, em Word e PDF</summary>

Faz o resumo de uma cadeira, de um bloco ou de alguns temas a partir da `wiki/`, do detalhe em `raw/` (slides, livros, fichas, resoluções) e do mapa de exames, com espaço proporcional ao peso de cada tema nos exames: definições, fórmulas (equações nativas do Word), métodos passo a passo, exemplos resolvidos, erros comuns e as perguntas reais de exame de cada tema. Mostra o índice para aprovação antes de escrever, guarda uma pasta por âmbito sem data no nome (`estudo/resumo-<âmbito>/`) com a versão e a data na capa e no rodapé, e renderiza com pandoc e Word — se o pandoc não estiver instalado, pergunta se o deve instalar.

→ [`SKILL.md`](skills/study-summary/SKILL.md)

</details>

<details>
<summary><b><code>mock-exam</code></b> — Cria simulados de exame com enunciado e correção separados</summary>

Imita a época escolhida (normal, recurso, especial, modelo) com a mesma duração, consulta, cotações e estilo do professor, a partir do mapa de exames; escolhe os temas pelo peso e pelas tendências e escreve perguntas novas ou variantes de perguntas reais que se respondem só com a matéria da KB — ou, em modo compilação, junta perguntas reais de anos diferentes. Mostra o plano do simulado para aprovação, gera o enunciado (sem pistas) e a correção (resposta-modelo, critérios de cotação, erros que descontam) em Word/PDF numa pasta numerada (`estudo/simulado-<âmbito>-<n>/`), e verifica a correr as respostas de cálculo e código (Python, SWI-Prolog…), marcando o que não pôde verificar.

→ [`SKILL.md`](skills/mock-exam/SKILL.md)

</details>

<details>
<summary><b><code>solve-exam</code></b> — Resolve exames e fichas só com a matéria da cadeira</summary>

Resolve um exame antigo, uma ficha, perguntas do catálogo ou um enunciado colado/fotografado com os métodos, a notação e a linguagem da cadeira, citando a fonte de cada resposta. Para cada pergunta dá a resposta a escrever na prova (do tamanho da cotação e do tempo), o porquê passo a passo e o que vale pontos; segue a resolução oficial quando existe e assinala onde discorda, avisa e pergunta antes de responder ao que está fora da matéria da KB, e verifica a correr cálculos e código. Tem modo só pistas, responde no chat a uma pergunta solta e guarda em Word/PDF versionado (`estudo/resolucao-<enunciado>/`).

→ [`SKILL.md`](skills/solve-exam/SKILL.md)

</details>

<details>
<summary><b><code>correct-attempt</code></b> — Corrige as tuas tentativas e regista os pontos fracos</summary>

Lê a tua resolução (foto, scan, PDF ou texto), confirma contigo a escrita à mão duvidosa antes de corrigir e corrige pergunta a pergunta e critério a critério, com a exigência do professor, contra a melhor referência disponível (soluções do simulado, resolução oficial, `solve-exam` ou uma feita na hora). Classifica cada erro (conceito, cálculo, incompleto, interpretação, notação, por responder), dá uma nota estimada na escala da cadeira e guarda a avaliação em `estudo/progresso-<cadeira>/tentativas/`. Reconstrói (junto com as sessões do `quiz`) o registo de progresso por tema (🔴/🟡/🟢, tendência, erros recorrentes) e a prioridade de estudo cruzada com o peso nos exames — que o `mock-exam` usa para simulados focados nos pontos fracos e o `study-summary` para mostrar o teu estado em cada tema.

→ [`SKILL.md`](skills/correct-attempt/SKILL.md)

</details>

<details>
<summary><b><code>quiz</code></b> — Tutor no chat que te faz perguntas, focado nos pontos fracos</summary>

Faz perguntas uma a uma no chat — rápidas (definições, escolha múltipla com botões, verdadeiro/falso, contas curtas) ou ao estilo do exame — focadas nos teus pontos fracos (do registo de progresso) ou no que pesa mais nos exames. É socrático: quando erras dá uma pista e deixa-te tentar outra vez antes de explicar, com a fonte; adapta a dificuldade às tuas respostas e volta mais tarde aos temas em que falhaste. Perguntas e respostas vêm da KB e as contas são verificadas antes de perguntar. Guarda cada sessão em `estudo/progresso-<cadeira>/quizzes/` e atualiza o registo — o quiz só decide o estado de um tema enquanto há menos de duas tentativas de exame.

→ [`SKILL.md`](skills/quiz/SKILL.md)

</details>

<details>
<summary><b><code>flashcards</code></b> — Cria flashcards para o Anki</summary>

Gera cartões de um só facto (básicos e cloze) a partir da `wiki/` e da formulação exata do `raw/`, em maior número nos temas que mais saem nos exames e nos teus pontos fracos, cada um com a fonte no verso e etiquetas (cadeira, tema, frequência no exame, `fraco`). Mostra a contagem por tema e uma amostra antes de gerar tudo, guarda a fonte legível em `estudo/flashcards-<âmbito>/` e exporta, com `scripts/anki_export.py`, para o ficheiro de texto do Anki (sem instalar nada) ou para `.apkg` com imagens. Os cartões têm ids estáveis: reimportar uma versão nova atualiza-os no Anki em vez de os duplicar, e os removidos saem com uma etiqueta para os apagares.

→ [`SKILL.md`](skills/flashcards/SKILL.md)

</details>

<details>
<summary><b><code>study-plan</code></b> — Faz o plano de estudo, dia a dia, até aos exames</summary>

Pergunta as datas dos exames, as horas que tens por dia e como estudas (mais leitura ou exercícios, primeiro leitura e depois exercícios, blocos longos ou curtos…), e distribui o tempo por tema em proporção ao peso no exame × fraqueza (do registo de progresso) × tamanho, em fases — matéria, prática e reta final com simulados em condições de exame e correção — com flashcards diários, revisão espaçada e 10–15% de folga. Cada dia tem tarefas concretas com links e a skill a usar (resumo, perguntas do catálogo, quiz, simulado). Mostra o esboço antes de escrever, guarda o plano em markdown com checkboxes (sem Word/PDF) e, depois de perguntar, gera um `.ics` e/ou cria os eventos no teu calendário se tiveres um conector ativo (Google Calendar). Responde a "o que tenho hoje?" e replaneia a partir do que já fizeste.

→ [`SKILL.md`](skills/study-plan/SKILL.md)

</details>
