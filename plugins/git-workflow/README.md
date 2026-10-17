# `git-workflow` — Git & GitHub

Parte do [Syntraq](../../README.md) — *Power up your agents*.

Commits e pull requests num fluxo GitFlow para projetos pessoais. Cada passo que mexe no repositório — o commit, o push, o PR — só acontece depois de veres e aprovares o que vai ser feito.

## Instalação

```
/plugin marketplace add DiogoMMP/syntraq
/plugin install git-workflow@syntraq
```

## Skills

| Skill | O que faz |
| :--- | :--- |
| [`commit-push`](skills/commit-push/SKILL.md) | Cria commits (Conventional Commits) e faz push, seguindo GitFlow |
| [`create-pr`](skills/create-pr/SKILL.md) | Abre um pull request preenchendo o template do repositório |

## Em detalhe

<details>
<summary><b><code>commit-push</code></b> — Cria commits (Conventional Commits) e faz push, seguindo GitFlow</summary>

Lê o estado do repositório, valida a branch contra o modelo GitFlow (`main`/`develop`/`feature`/`bugfix`/`release`/`hotfix`, e também os prefixos do Conventional Commits como `fix/`, `chore/`, `docs/` ou `refactor/`) — ou contra o modelo que o `AGENTS.md`/`CLAUDE.md` do repositório descreve — agrupa o diff em commits coerentes e mostra a(s) mensagem(ns) propostas no chat, aguardando validação explícita antes de commitar — e pergunta separadamente, só depois, se deve fazer push. Quando há uma issue do GitHub associada (no nome da branch ou na conversa), é referenciada (`Refs: #12`); quando não há, não se pede uma.

→ [`SKILL.md`](skills/commit-push/SKILL.md)

</details>

<details>
<summary><b><code>create-pr</code></b> — Abre um pull request preenchendo o template do repositório</summary>

Confirma que a branch já está commitada e pushed (nunca commita nem faz push), resolve a branch base a partir do GitFlow, lê primeiro o template de PR do repositório (ou, se o repositório não tiver nenhum, usa o template por defeito que vem com a skill, adaptando os comandos de build e testes ao projeto) e preenche-o com base no diff real — em português por defeito — linkando os registos em `docs/changes/` que a branch toca. Mostra o título e o corpo completos e só corre `gh pr create` depois de aprovação explícita.

→ [`SKILL.md`](skills/create-pr/SKILL.md)

</details>
