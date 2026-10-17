# ai-skills

Plugin de [Claude Code](https://code.claude.com) com uma coleção pessoal de skills.

## Instalação

Este repositório é uma marketplace com 3 plugins:

| Plugin | Skills |
| :--- | :--- |
| `git-workflow` | `commit-push`, `create-pr` |
| `dev-tools` | `implement-change`, `clean-architecture`, `write-tests`, `create-readme`, `create-agents-md` |
| `knowledge-base` | `knowledge-base`, `compile-wiki`, `capture-note`, `adr-new`, `resume`, `wiki-lint` |

```
/plugin marketplace add DiogoMMP/ai-skills
/plugin install git-workflow@ai-skills
/plugin install dev-tools@ai-skills
/plugin install knowledge-base@ai-skills
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
| [create-pr](plugins/git-workflow/skills/create-pr/SKILL.md) | Abre um pull request preenchendo o template do repositório | Confirma que a branch já está commitada e pushed (nunca commita nem faz push), resolve a branch base a partir do GitFlow, lê primeiro o template de PR do repositório (ou, se o repositório não tiver nenhum, usa o template por defeito que vem com a skill, adaptando os comandos de build e testes ao projeto) e preenche-o com base no diff real — em português por defeito — linkando os registos em `docs/changes/` que a branch toca. Mostra o título e o corpo completos e só corre `gh pr create` depois de aprovação explícita. |

### `dev-tools` — Desenvolvimento

| Skill | Resumo | Descrição |
| :--- | :--- | :--- |
| [implement-change](plugins/dev-tools/skills/implement-change/SKILL.md) | Implementa uma feature, bugfix ou hotfix ponta a ponta, com registo escrito | Aceita o pedido em qualquer formato (texto livre, issue, página de wiki, spec, screenshots), determina o tipo de mudança (feature/bugfix/hotfix), investiga o projeto, propõe um plano no chat e espera aprovação, escreve a spec em `docs/changes/<tipo>/<PREFIXO><NNNN>-<slug>/README.md` antes de tocar em código — separado de `docs/wiki/`/`docs/notes/` para não poluir uma knowledge base que viva no mesmo `docs/` — implementa, corre a verificação própria do projeto e fecha com um `RESULT.md` honesto sobre o que realmente aconteceu, desvios incluídos. Não commita nem abre PR — isso fica para `commit-push` e `create-pr`. Créditos: [@michelgomessilva](https://github.com/michelgomessilva). |
| [create-readme](plugins/dev-tools/skills/create-readme/SKILL.md) | Escreve ou reescreve o README.md raiz no formato da casa | Investiga o repositório (stack, arquitetura, módulos, portas, testes, CI) e preenche um template fixo — badges, índice, stack técnica, diagrama de arquitetura, layout anotado, getting started, testes, contribuição — só com factos que consegue provar em ficheiros reais. Nunca inventa comandos, versões ou URLs, remove secções sem evidência em vez de as inventar, e nunca escreve nada que pareça um segredo. Mostra o rascunho completo e espera aprovação antes de escrever o ficheiro. |
| [create-agents-md](plugins/dev-tools/skills/create-agents-md/SKILL.md) | Escreve ou atualiza o `AGENTS.md` do repositório, em conjunto contigo | Cria o ficheiro de instruções que todos os agentes leem (Claude Code, Codex, Cursor, Copilot…) a partir de um primeiro rascunho do `/init` e do que consegue provar no repositório — scripts, CI (o que corre e o que não corre, branch guards, título de PR, versões automáticas), histórico de branches e commits, padrões do código — e vai perguntando, secção a secção, o que o código não diz: armadilhas, o que nunca fazer, língua e o fluxo git (commits na `main` ou não, `develop`, branches `feature`/`fix`/`hotfix`), com uma recomendação. Só fica o que faria um agente errar se faltasse. Garante que o Claude Code o lê (`@AGENTS.md` num `CLAUDE.md`), não mexe no bloco da knowledge base, mostra o ficheiro completo (ou o diff, ao atualizar) e espera aprovação antes de escrever. |
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


## Licença

MIT — ver [LICENSE](LICENSE).
