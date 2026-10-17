---
name: commit-push
description: "Create git commits (and optionally push) following a GitFlow-style branching strategy for personal projects. Checks whether the change warrants a version bump (package.json, a .csproj, pyproject.toml, plugin.json, etc. — skipped entirely when the repo already versions automatically via semantic-release/GitVersion/MinVer/etc.) before writing Conventional Commits messages, ALWAYS shows the full proposed message(s) to the user and waits for explicit validation before committing, and ALWAYS asks separately before pushing. Use whenever the user wants to commit, stage and commit, split work into commits, write a commit message, or push — e.g. 'commit', 'commit this', 'faz commit', 'commit e push', 'commita as alterações', 'push', 'write the commit message', 'guarda isto no git'. Also use when finishing a task and the user asks to save the work to git."
allowed-tools: ["Bash", "AskUserQuestion", "Read", "Grep", "Glob"]
---

# Commit & Push — GitFlow

Two hard gates in this skill. Never skip either, never merge them into one:

1. **Message gate** — propose the commit message(s) in chat, wait for the user's explicit OK.
2. **Push gate** — after committing, ask with `AskUserQuestion` whether to push. No push without a clear yes.

Committing or pushing in the same turn as the proposal is a failure of this skill, even if the user said "commit and push" up front. "Commit and push" authorizes the *flow*, not the message you have not shown them yet.

---

## Step 1 — Read the repo state

Run these in one batch (read-only, cheap):

```bash
git status --porcelain=v1 --branch
git diff --stat
git diff
git diff --staged
git log --oneline -10
git branch --show-current
git remote -v
```

Also read the repo's `CLAUDE.md` / `AGENTS.md` if present. **Repo-level conventions win over the defaults in this skill** (commit style visible in `git log`, branch policy, etc.).

If there is nothing to commit, say so and stop. Do not invent work.

---

## Step 2 — Validate the branch against GitFlow

| Branch | Pattern | Purpose |
| --- | --- | --- |
| Main | `main` | Production / stable releases |
| Develop | `develop` | Integration of features before a release |
| Feature | `feature/<slug>` | New functionality |
| Bugfix | `bugfix/<slug>` | Fixing something in a release candidate before it ships |
| Release | `release/<version>` | Preparing a version (e.g. `release/1.2.0`) |
| Hotfix | `hotfix/<slug>` | Urgent fixes on top of `main` |
| Typed work branch | `fix/`, `chore/`, `docs/`, `refactor/`, `test/`, `ci/`, `build/`, `perf/`, `style/`, `revert/` + `<slug>` | The Conventional Commits types used as prefixes; `fix/` is the usual bug-fix branch in repos that don't cut release branches |

A branch may optionally reference a GitHub issue by leading its slug with the number (e.g. `feature/12-dark-mode`) — this is a convenience, never a requirement. Personal projects rarely track every change as an issue; don't ask for one.

**The repo's own workflow wins.** If `AGENTS.md` or `CLAUDE.md` describes the branching model (direct commits on `main`, no `develop`, which prefixes exist), follow it over this table — and over the checks below.

Checks:

- **On `feature/*`, `bugfix/*`, `release/*`, `hotfix/*` or a typed work branch (`fix/*`, `chore/*`, `docs/*`, …)** → proceed normally.
- **On `main` or `develop`** → this is where GitFlow expects PRs, not direct commits. Ask with `AskUserQuestion` before going further, offering: (a) create `feature/<slug>` from here and carry the changes over, (b) commit directly on this branch anyway. **Exception:** if the repo's `AGENTS.md` or `CLAUDE.md`, a project memory, or the user has already stated that this repo commits directly to `main`, skip the question and commit — do not re-ask every time.
- **Detached HEAD** → stop and tell the user; do not commit.

If the user picks (a): `git switch -c feature/dark-mode` (features branch from `develop`, hotfixes from `main`). Never create the branch without being asked to.

---

## Step 3 — Decide the commit split

Read the actual diff and group it by intent, not by file:

- One coherent change → one commit.
- Unrelated changes in the same working tree → **several commits**, each self-contained and independently reviewable (e.g. a `fix:` kept apart from the `chore:` that reformatted config).
- Never mix a refactor with a behaviour change in one commit when they can be separated.

### When the repo has pre-commit hooks, split much finer

Check first — `ls .pre-commit-config.yaml .husky/ .githooks/`, or `git config core.hooksPath`. When formatters or linters run on commit, **split as far as the work allows, even within a single coherent change**, as long as each commit still builds and no two of them fight over the same lines. A large commit is not merely harder to review; with hooks it actively misbehaves:

- **Hook cost scales with the staged set, superlinearly.** pre-commit batches filenames and runs a formatter once per batch — twice per batch when it finds something to fix. A 270-file commit became 14 batches × 2 runs and took over ten minutes; the same work split eight ways is a handful of files per run.
- **A long hook run gets killed, and killed runs leave orphans.** Tool timeouts fire; the MSBuild / ESLint / compiler daemons the formatter spawned stay resident and the next attempt starts on a loaded machine. Recorded: nine orphaned MSBuild nodes holding ~900 MB after one killed run.
- **The stash/restore cycle is the real hazard, and it scales with what is left unstaged.** pre-commit stashes unstaged changes, lets hooks rewrite staged files, then restores. When the restore conflicts it prints `Rolling back fixes...` and reapplies the patch over the tree — and files nobody touched come back mangled. Recorded: a solution file silently lost three projects and four `.csproj` lost a shared project reference, three separate times, caught only because the build went from 0 to 493 errors.

Concretely:

- **Commit the enabling change on its own, first** — the dependency swap, the config or hook change, the new shared abstraction — then the code that uses it. Each lands with a small staged set, and a hook config fix lands before the commits that depend on it.
- **Split mechanical sweeps by layer or module** even when they are one logical change: the generated/library layer, then the callers, then the tests. Each is a normal-sized, reviewable commit.
- **Keep the working tree clean at commit time.** Stage everything that belongs to the commit, or move what does not belong out of the repo first. **Nothing unstaged means no stash, and no stash means the rollback path cannot fire.** This is the single most effective guard.
- **Run the formatter yourself before staging** (`dotnet format`, `prettier --write`, `ruff format`) so the hooks find nothing to fix. Hooks that change nothing never trigger the rollback.
- **After every commit on such a repo, verify the files you did not touch.** Compare the shared solution/project/lock files against the previous commit. If one changed and you did not change it, restore it and say so — never assume the tooling was right.

Do **not** split so far that a commit fails to build, and never produce a sequence with a broken intermediate state. Between "one big commit" and "a broken bisect", prefer the big commit — but on a hooked repo that choice should be rare.

**Never reach for `--no-verify`** to escape any of this. If the hooks cannot be satisfied, the cause is either your input or a defect in the hook configuration; find out which, and say so.

Never `git add -A` blindly. Before staging, scan the untracked/modified list for things that must not be committed: `.env*`, `*.pem`, `*.key`, credentials, tokens, `node_modules/`, build output (`dist/`, `bin/`, `obj/`, `.next/`), local scratch files, large binaries. Flag anything suspicious to the user instead of staging it, and say so if `.gitignore` is missing an entry for it.

---

## Step 4 — Check whether a version bump belongs in this commit

Not every commit bumps a version — most don't. Check before assuming either way.

1. **Look for automatic versioning first.** If the repo already derives its version from git tags/history, this skill does not touch a version field at all — a manual bump would fight the tool. Evidence: `semantic-release` config (`.releaserc*`, `release.config.*`, a `release` key in `package.json`), Changesets (`.changeset/config.json`), GitVersion (`GitVersion.yml`/`.yaml`), MinVer or Nerdbank.GitVersioning (a `<PackageReference Include="MinVer"` / `"Nerdbank.GitVersioning"` in a `.csproj`, or a `version.json`). If any of these are present, **skip this step entirely** — don't ask, don't touch the version.

2. **Otherwise, find the version-holding file(s)**, if any exist in this repo: `package.json` (`version`), `*.csproj` / `Directory.Build.props` (`<Version>`, `<AssemblyVersion>`, `<FileVersion>`), `pyproject.toml` (`[project] version` / `[tool.poetry] version`), `Cargo.toml` (`[package] version`), `composer.json` (`version`), `gradle.properties` / `build.gradle*` (`version`), `.claude-plugin/plugin.json` (`version`), a standalone `VERSION` file, or a `CHANGELOG.md` with an `[Unreleased]` section (Keep a Changelog style) worth moving into a dated one. If none of these exist, there's nothing to bump — move on without comment.

3. **Decide whether this commit is the kind that bumps it.** Bumping usually belongs on a `release/*` branch when cutting a release, or — for a small personal tool/plugin that versions per meaningful change rather than per release — on any branch when the change is user-facing. It usually does **not** belong on routine mid-development commits, docs-only changes, or refactors with no externally visible effect; those wait for the release step.
   - **On `release/*`** → ask. This is very likely the moment to bump.
   - **Elsewhere** → only raise it when the diff is user-facing (a `feat`/`fix`, per the type you'll use in Step 5) **and** the repo's own history shows it bumps per-commit rather than only on release branches/tags (`git log -p -- <version file>` shows the pattern). If history is inconclusive, or this would be the first commit ever touching that file, ask once rather than guessing either way.

4. **When asking, use `AskUserQuestion`.** Show the current version and offer patch / minor / major — with a recommendation derived from the Conventional Commits type (`fix` → patch, `feat` → minor, a `BREAKING CHANGE` footer or `!` → major) — plus "don't bump". Semver is a judgment call about the actual change, not something to infer from a diff and apply silently.

5. **If the user says bump:** update every version file that belongs to the package being changed, so they don't drift — and only those: in a repo with several packages or plugins (a monorepo, a plugin marketplace), another package that happens to have the same version number is not part of this release. Prefer the ecosystem's own bump command when one exists (`npm version --no-git-tag-version <bump>`, `cargo set-version`, `poetry version <bump>`) over hand-editing, and hand-edit only where no such command exists (e.g. a `.csproj`'s `<Version>`, or `.claude-plugin/plugin.json`). Decide whether it's its own commit (`chore(release): bump version to X.Y.Z` — the norm when cutting a release on `release/*`) or folded into the feature/fix commit it belongs to (when the project bumps per-change), and say which and why when you show the proposal in Step 6.

---

## Step 5 — Write the message(s)

### Format

```
<type>(<scope>): <subject>

<body — why, not what. wrapped at ~72 chars. bullets allowed.>

Refs: #12
Co-Authored-By: Claude <model> <noreply@anthropic.com>
```

- **type** — Conventional Commits: `feat`, `fix`, `chore`, `docs`, `refactor`. `test`, `perf`, `ci`, `build`, `style` are acceptable extensions when they fit better.
- **scope** — optional, the code area touched (`auth`, `checkout`, `pipeline`).
- **subject** — imperative mood ("add", not "added"/"adds"), lowercase start, no trailing period, ≤ 72 chars. Describes the change, not the process ("fix null check on cart total", never "changes requested in review").
- **body** — optional; include it when the *why* isn't obvious from the subject. Explain intent, trade-offs, and anything a reviewer would otherwise have to ask. Skip it for trivial commits.
- **Refs** — check whether this change has an associated GitHub issue: derivable from the branch name (e.g. `feature/12-dark-mode` → `#12`) or mentioned anywhere in the conversation. **If one exists, it must be referenced** — `Refs: #12`, or `Closes: #12` only if the user says the issue is done; don't drop a known issue silently. Only the *absence* of one is optional to leave as-is — never ask the user to open an issue just to fill this line.
- **language** — commit messages in **English** by default, regardless of the chat language — unless the repo's `AGENTS.md`/`CLAUDE.md` names another language for commits, or its `git log` clearly shows one. Then write in that language (types and scopes stay as the repo uses them).

### The Co-Authored-By trailer — exact rules

- Present on **every** commit, including squashes, fixups, amends and merge commits.
- Blank line before the trailer block.
- Format: `Co-Authored-By: Claude <model name> <noreply@anthropic.com>` where the **model name is plain text, unbracketed**, and the **only** angle brackets on the line wrap the email.
- Use the concrete model when known, e.g.:

  ```
  Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
  ```

- If the model name is genuinely unknown, fall back to `Co-Authored-By: Claude <noreply@anthropic.com>`.
- On rewrites (amend / rebase / squash), keep the trailers already present in the message.

**Wrong — never produce these:**

```
Co-Authored-By: Claude <Opus 5> noreply@anthropic.com     ← brackets on the name
Co-Authored-By: Claude Opus 5 noreply@anthropic.com       ← email not bracketed
Co-authored-by: claude opus 5 <noreply@anthropic.com>     ← wrong casing
```

### Forbidden in commit messages

- **No** `🤖 Generated with [Claude Code](https://claude.com/claude-code)` line. Ever. Not in the body, not in the footer.
- No emoji-only subjects, no `Generated by`, no tool advertising, no "as requested by the user".
- No `Signed-off-by` unless the repo requires DCO.

*(Scope note: the `🤖 Generated with` line still belongs at the end of **pull request bodies** — see `create-pr`. This skill's ban covers commit messages only.)*

---

## Step 6 — MESSAGE GATE: show and wait

Print the message(s) in chat **verbatim** — exactly the bytes that will land in git — in a fenced block per commit, each with the files it will stage:

> **Commit 1 of 2** — `src/cart/total.ts`, `src/cart/total.test.ts`
> ```
> fix(cart): guard against null line prices in the total
>
> A promo line with no price made the subtotal NaN and blanked the summary. Treat a missing price as 0 and cover it with a test.
>
> Refs: #12
> Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
> ```

Then ask for validation and **end the turn**. Do not run `git commit` in this turn.

Accept edits: if the user changes wording, the split, or the files in a commit, re-show the revised proposal and wait again. Only an explicit approval ("ok", "sim", "avança", "commit") opens the gate.

---

## Step 7 — Commit

Stage exactly the files listed for each commit (`git add -- <paths>`), then commit each one with a heredoc so the message keeps its line breaks:

```bash
git commit -F - <<'MSG'
fix(cart): guard against null line prices in the total

A promo line with no price made the subtotal NaN and blanked the
summary. Treat a missing price as 0 and cover it with a test.

Refs: #12
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
```

Rules:

- Never `--no-verify`. If a hook fails, report it and fix the cause — don't bypass it.
- Never `--amend`, `rebase`, `reset --hard`, or `checkout --` over the user's changes unless they explicitly asked. If a pre-commit hook reformatted files, `git add` them and commit again.
- If a commit fails, stop and report — don't silently retry with a different approach.
- Verify with `git log --format='%B' -1` that the trailer came out right and no forbidden line slipped in.

---

## Step 8 — PUSH GATE: ask, then push

Never push implicitly. Ask with `AskUserQuestion`:

- Question: e.g. "Fiz N commit(s) em `feature/dark-mode`. Faço push para `origin`?"
- Options: **"Sim, faz push"** / **"Não, fica local"**.

On yes:

```bash
git push                                  # branch already tracks a remote
git push -u origin feature/dark-mode      # first push of a new branch
```

- Never `--force`. `--force-with-lease` only when the user explicitly asks for a force push.
- If the push is rejected as non-fast-forward, **stop and report**. Don't pull/rebase/merge on your own initiative — ask what they want.
- If `main`/`develop` is protected and the push is rejected, report it and mention the PR route.

On no: confirm the commits are local, and give them the push command for later.

---

## Step 9 — Report

Short and factual:

- The commits created — `git log --oneline -N` output.
- Branch, and whether it was pushed or is still local.
- **Version**, if Step 4 changed one — old → new, which file(s), and whether it landed in its own commit or folded into another. Say explicitly if you checked and decided **not** to bump, and why.
- Anything left uncommitted on purpose (and why), or files you refused to stage.
- If a PR is the next GitFlow step (`feature/*` → `develop`, `release/*` → `main`), mention it — but only open one if the user asks.
