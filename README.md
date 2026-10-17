# ai-skills

Plugin de [Claude Code](https://code.claude.com) com uma coleção pessoal de skills.

## Instalação

Este repositório é uma marketplace com 4 plugins:

| Plugin | Skills |
| :--- | :--- |
| `git-workflow` | `commit-push`, `create-pr` |
| `dev-tools` | `implement-change`, `clean-architecture`, `write-tests`, `create-readme` |
| `knowledge-base` | `knowledge-base`, `compile-wiki`, `capture-note`, `adr-new`, `resume`, `wiki-lint` |
| `study` | `exam-map`, `study-summary`, `mock-exam`, `solve-exam`, `correct-attempt`, `quiz`, `flashcards`, `study-plan` |

```
/plugin marketplace add DiogoMMP/ai-skills
/plugin install git-workflow@ai-skills
/plugin install dev-tools@ai-skills
/plugin install knowledge-base@ai-skills
/plugin install study@ai-skills
```

Localmente, durante desenvolvimento: `claude --plugin-dir ./plugins/dev-tools`

## Estrutura

```
ai-skills/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── <plugin>/
        ├── .claude-plugin/plugin.json
        └── skills/<skill>/SKILL.md
```

## Skills

### `git-workflow` — Git & GitHub

| Skill | Resumo | Descrição |
| :--- | :--- | :--- |
| [commit-push](plugins/git-workflow/skills/commit-push/SKILL.md) | Cria commits (Conventional Commits) e faz push, seguindo GitFlow | Lê o estado do repositório, valida a branch contra o modelo GitFlow (`main`/`develop`/`feature`/`bugfix`/`release`/`hotfix`), agrupa o diff em commits coerentes e mostra a(s) mensagem(ns) propostas no chat, aguardando validação explícita antes de commitar — e pergunta separadamente, só depois, se deve fazer push. Uma issue do GitHub pode ser referenciada (`Refs: #12`) mas nunca é obrigatória. |
| [create-pr](plugins/git-workflow/skills/create-pr/SKILL.md) | Abre um pull request preenchendo o template do repositório | Confirma que a branch já está commitada e pushed (nunca commita nem faz push), resolve a branch base a partir do GitFlow, lê primeiro o template de PR do repositório e preenche-o com base no diff real — em português por defeito — linkando os registos em `docs/changes/` que a branch toca. Mostra o título e o corpo completos e só corre `gh pr create` depois de aprovação explícita. |

### `dev-tools` — Desenvolvimento

| Skill | Resumo | Descrição |
| :--- | :--- | :--- |
| [implement-change](plugins/dev-tools/skills/implement-change/SKILL.md) | Implementa uma feature, bugfix ou hotfix ponta a ponta, com registo escrito | Aceita o pedido em qualquer formato (texto livre, issue, página de wiki, spec, screenshots), determina o tipo de mudança (feature/bugfix/hotfix), investiga o projeto, propõe um plano no chat e espera aprovação, escreve a spec em `docs/changes/<tipo>/<PREFIXO><NNNN>-<slug>/README.md` antes de tocar em código — separado de `docs/wiki/`/`docs/notes/` para não poluir uma knowledge base que viva no mesmo `docs/` — implementa, corre a verificação própria do projeto e fecha com um `RESULT.md` honesto sobre o que realmente aconteceu, desvios incluídos. Não commita nem abre PR — isso fica para `commit-push` e `create-pr`. |
| [create-readme](plugins/dev-tools/skills/create-readme/SKILL.md) | Escreve ou reescreve o README.md raiz no formato da casa | Investiga o repositório (stack, arquitetura, módulos, portas, testes, CI) e preenche um template fixo — badges, índice, stack técnica, diagrama de arquitetura, layout anotado, getting started, testes, contribuição — só com factos que consegue provar em ficheiros reais. Nunca inventa comandos, versões ou URLs, remove secções sem evidência em vez de as inventar, e nunca escreve nada que pareça um segredo. Mostra o rascunho completo e espera aprovação antes de escrever o ficheiro. |
| [clean-architecture](plugins/dev-tools/skills/clean-architecture/SKILL.md) | Cria (ou reorganiza) um projeto em Clean Architecture | Estrutura um projeto novo em camadas Domain/Application/Infrastructure/Api (+ CrossCutting opcional), ou audita um já existente e propõe um plano de reorganização — adaptando projetos/pastas/ferramentas ao stack real (.NET, Node, Python, Java, Go, ...) em vez de copiar um template. Pergunta primeiro as decisões estruturais (CQRS ou não, um serviço ou vários, base de dados e migrations, Docker, jobs, auth, alcance dos testes) e só cria/move depois de aprovação. Nunca mexe em `docs/` (isso é o `implement-change`/`knowledge-base`) nem commita. |
| [write-tests](plugins/dev-tools/skills/write-tests/SKILL.md) | Escreve testes unitários e/ou de integração, em qualquer stack | Pergunta primeiro o alvo (um ficheiro/função/feature à tua escolha, ou uma varredura de cobertura ao projeto) e o nível (unit, integração a nível de serviço/API, ou ambos — sem E2E/browser). Deteta a framework de testes e convenções já usadas (ou pergunta qual montar), resolve como subir dependências reais para testes de integração (Testcontainers, docker-compose existente, host de testes em processo), escreve os menos testes possível que provem o comportamento — em vez de um por cada permutação trivial, já que cada teste é um custo recorrente no CI/CD — corre-os para provar que passam, e sinaliza — sem gerar sozinho — outras lacunas de cobertura que note pelo caminho. Nunca mexe em `docs/` nem commita. |

### `knowledge-base` — Knowledge base pessoal

Estas skills implementam o fluxo `raw/` → `wiki/` compilado por LLM descrito por [Andrej Karpathy](https://x.com/karpathy/status/2039805659525644595) na nota ["LLM Knowledge Bases"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — a inspiração original para esta abordagem.

| Skill | Resumo | Descrição |
| :--- | :--- | :--- |
| [knowledge-base](plugins/knowledge-base/skills/knowledge-base/SKILL.md) | Cria a estrutura de pastas de uma knowledge base pessoal | Cria a estrutura de pastas de uma knowledge base pessoal, em dois modos: **research** (estilo Karpathy: `raw/` + `wiki/` + `outputs/` + `tools/`, para quando há muito material externo a ingerir) ou **code** (mais leve, `wiki/` + `notes/`, pensado para repos de código pessoais, alimentado por notas soltas e pelo git log em vez de um `raw/`). Em modo research o `raw/` não tem regras de estrutura, nada assume que a pasta é um repositório git, `notes/` funciona como inbox (as compiladas são arquivadas em `notes/<área>/`) e `outputs/<área>/` divide-se por finalidade — estudo, entregas, respostas e trabalho versionado em pastas `vN/` — com a wiki como única fonte de verdade. Todos os templates são escritos na língua da KB. Pergunta o modo, a pasta de destino, opcionalmente se existe modelo de domínio a documentar (modo code), e se quer ligar a um vault geral partilhado (via junction `wiki/_geral`, visível no mesmo grafo do Obsidian). |
| [compile-wiki](plugins/knowledge-base/skills/compile-wiki/SKILL.md) | Compila/atualiza a `wiki/` a partir de notas e do git | Faz a compilação, seguindo o modo definido no `KB_GUIDE.md`: em modo research lê `raw/`, resume e organiza em artigos por conceito; em modo code lê `notes/` (ficheiros com frontmatter `status: pending`/`compiled`) e tudo o que houver de novo no git — commits, issues e pull requests (via `gh`, se disponível) — desde o último `last_compiled_at`, e regenera sempre por inteiro `wiki/Estrutura.md` (estrutura de pastas, stack técnica, pontos de entrada e o modelo de domínio, se estiver registado). Em ambos os modos cria backlinks e mantém `wiki/index.md` atualizado — os artigos de decisão de forma incremental, a `Estrutura.md` sempre do zero — e, depois de compilar cada nota, move-a da inbox para `notes/<área>/`. Respeita o tipo de cada nota: as tuas opiniões e decisões, mensagens de outras pessoas atribuídas a quem as escreveu e respostas de IA marcadas como não verificadas. |
| [capture-note](plugins/knowledge-base/skills/capture-note/SKILL.md) | Grava rapidamente uma nota solta em `notes/` | Grava rapidamente um pensamento na inbox de `notes/` com o frontmatter certo (`status: pending` e, quando é evidente, o tipo: decisão, pergunta, resposta de IA ou mensagem de outra pessoa como o perito ou o professor), sem organizar nada — isso fica para o `compile-wiki`. |
| [adr-new](plugins/knowledge-base/skills/adr-new/SKILL.md) | Cria uma nota ADR de decisão arquitetural | Cria uma nota estilo ADR (Contexto/Decisão/Consequências) em `notes/`, útil para documentar uma decisão arquitetural no momento em que é tomada. |
| [resume](plugins/knowledge-base/skills/resume/SKILL.md) | Briefing para retomar um projeto pessoal parado | Briefing só de leitura: lê `wiki/Estrutura.md` (ou `index.md`), notas pendentes, e atividade git recente (incluindo alterações por commitar), e resume "onde ficaste" com sugestão de próximo passo. |
| [wiki-lint](plugins/knowledge-base/skills/wiki-lint/SKILL.md) | Health check da `wiki/` (links partidos, órfãos, etc.) | Health check da `wiki/`: links partidos, artigos órfãos (não referenciados no `index.md`), referências desatualizadas a ficheiros/decisões que já não existem, entradas soltas em `wiki/sources.md`/`notes/`, notas fora do sítio (compiladas na inbox ou pendentes no arquivo), outputs fora da estrutura ou sem linha no índice, e conteúdo repetido entre `outputs/` e a wiki. Reporta primeiro, só corrige o que for aprovado. |


### `study` — Estudo

Skills de estudo que trabalham por cima de uma knowledge base em modo research (criada pelo `knowledge-base`): leem o que já está em `raw/` e na `wiki/`, sem impor nenhuma estrutura ao `raw/`, e escrevem o conhecimento na `wiki/`.

| Skill | Resumo | Descrição |
| :--- | :--- | :--- |
| [exam-map](plugins/study/skills/exam-map/SKILL.md) | Mapeia o que sai nos exames de uma cadeira | Descobre os exames antigos em `raw/` pelo caminho, nome e conteúdo (exames, exame modelo, testes e resoluções), mostra a lista para confirmares na primeira vez, lê-os (com OCR quando são digitalizados) e classifica cada pergunta pelos artigos da própria wiki. Escreve na `wiki/` um artigo de exames — formato, tabela tema × exame com o peso de cada tema, ranking 🔥/⚠️/📎, tendências, tipos de pergunta, perguntas repetidas, estilo do professor e prioridades de estudo marcadas como interpretação — e um catálogo de perguntas com ids estáveis, de onde as outras skills de estudo tiram perguntas reais. Atualiza o artigo de avaliação que já exista em vez de criar outro, regista os exames em `wiki/sources.md`, é incremental (só lê exames novos) e assinala análises repetidas em `outputs/`. |
| [study-summary](plugins/study/skills/study-summary/SKILL.md) | Escreve um resumo completo para imprimir, em Word e PDF | Faz o resumo de uma cadeira, de um bloco ou de alguns temas a partir da `wiki/`, do detalhe em `raw/` (slides, livros, fichas, resoluções) e do mapa de exames, com espaço proporcional ao peso de cada tema nos exames: definições, fórmulas (equações nativas do Word), métodos passo a passo, exemplos resolvidos, erros comuns e as perguntas reais de exame de cada tema. Mostra o índice para aprovação antes de escrever, guarda uma pasta por âmbito sem data no nome (`estudo/resumo-<âmbito>/`) com a versão e a data na capa e no rodapé, e renderiza com pandoc e Word — se o pandoc não estiver instalado, pergunta se o deve instalar. |
| [mock-exam](plugins/study/skills/mock-exam/SKILL.md) | Cria simulados de exame com enunciado e correção separados | Imita a época escolhida (normal, recurso, especial, modelo) com a mesma duração, consulta, cotações e estilo do professor, a partir do mapa de exames; escolhe os temas pelo peso e pelas tendências e escreve perguntas novas ou variantes de perguntas reais que se respondem só com a matéria da KB — ou, em modo compilação, junta perguntas reais de anos diferentes. Mostra o plano do simulado para aprovação, gera o enunciado (sem pistas) e a correção (resposta-modelo, critérios de cotação, erros que descontam) em Word/PDF numa pasta numerada (`estudo/simulado-<âmbito>-<n>/`), e verifica a correr as respostas de cálculo e código (Python, SWI-Prolog…), marcando o que não pôde verificar. |
| [solve-exam](plugins/study/skills/solve-exam/SKILL.md) | Resolve exames e fichas só com a matéria da cadeira | Resolve um exame antigo, uma ficha, perguntas do catálogo ou um enunciado colado/fotografado com os métodos, a notação e a linguagem da cadeira, citando a fonte de cada resposta. Para cada pergunta dá a resposta a escrever na prova (do tamanho da cotação e do tempo), o porquê passo a passo e o que vale pontos; segue a resolução oficial quando existe e assinala onde discorda, avisa e pergunta antes de responder ao que está fora da matéria da KB, e verifica a correr cálculos e código. Tem modo só pistas, responde no chat a uma pergunta solta e guarda em Word/PDF versionado (`estudo/resolucao-<enunciado>/`). |
| [correct-attempt](plugins/study/skills/correct-attempt/SKILL.md) | Corrige as tuas tentativas e regista os pontos fracos | Lê a tua resolução (foto, scan, PDF ou texto), confirma contigo a escrita à mão duvidosa antes de corrigir e corrige pergunta a pergunta e critério a critério, com a exigência do professor, contra a melhor referência disponível (soluções do simulado, resolução oficial, `solve-exam` ou uma feita na hora). Classifica cada erro (conceito, cálculo, incompleto, interpretação, notação, por responder), dá uma nota estimada na escala da cadeira e guarda a avaliação em `estudo/progresso-<cadeira>/tentativas/`. Reconstrói (junto com as sessões do `quiz`) o registo de progresso por tema (🔴/🟡/🟢, tendência, erros recorrentes) e a prioridade de estudo cruzada com o peso nos exames — que o `mock-exam` usa para simulados focados nos pontos fracos e o `study-summary` para mostrar o teu estado em cada tema. |
| [quiz](plugins/study/skills/quiz/SKILL.md) | Tutor no chat que te faz perguntas, focado nos pontos fracos | Faz perguntas uma a uma no chat — rápidas (definições, escolha múltipla com botões, verdadeiro/falso, contas curtas) ou ao estilo do exame — focadas nos teus pontos fracos (do registo de progresso) ou no que pesa mais nos exames. É socrático: quando erras dá uma pista e deixa-te tentar outra vez antes de explicar, com a fonte; adapta a dificuldade às tuas respostas e volta mais tarde aos temas em que falhaste. Perguntas e respostas vêm da KB e as contas são verificadas antes de perguntar. Guarda cada sessão em `estudo/progresso-<cadeira>/quizzes/` e atualiza o registo — o quiz só decide o estado de um tema enquanto há menos de duas tentativas de exame. |
| [flashcards](plugins/study/skills/flashcards/SKILL.md) | Cria flashcards para o Anki | Gera cartões de um só facto (básicos e cloze) a partir da `wiki/` e da formulação exata do `raw/`, em maior número nos temas que mais saem nos exames e nos teus pontos fracos, cada um com a fonte no verso e etiquetas (cadeira, tema, frequência no exame, `fraco`). Mostra a contagem por tema e uma amostra antes de gerar tudo, guarda a fonte legível em `estudo/flashcards-<âmbito>/` e exporta, com `scripts/anki_export.py`, para o ficheiro de texto do Anki (sem instalar nada) ou para `.apkg` com imagens. Os cartões têm ids estáveis: reimportar uma versão nova atualiza-os no Anki em vez de os duplicar, e os removidos saem com uma etiqueta para os apagares. |
| [study-plan](plugins/study/skills/study-plan/SKILL.md) | Faz o plano de estudo, dia a dia, até aos exames | Pergunta as datas dos exames e as horas que tens por dia, e distribui o tempo por tema em proporção ao peso no exame × fraqueza (do registo de progresso) × tamanho, em fases — matéria, prática e reta final com simulados em condições de exame e correção — com flashcards diários, revisão espaçada e 10–15% de folga. Cada dia tem tarefas concretas com links e a skill a usar (resumo, perguntas do catálogo, quiz, simulado). Mostra o esboço antes de escrever, guarda o plano com checkboxes e em Word/PDF, e, depois de perguntar, gera um `.ics` e/ou cria os eventos no teu calendário se tiveres um conector ativo (Google Calendar). Responde a "o que tenho hoje?" e replaneia a partir do que já fizeste. |

## Licença

MIT — ver [LICENSE](LICENSE).
