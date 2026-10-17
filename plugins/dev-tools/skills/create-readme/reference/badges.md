# The badge wall

A block of static [shields.io](https://shields.io) badges directly under the `#` title, one per line, no blank lines between them, before the lead paragraph.

**Rules**

- **Static badges only.** `img.shields.io/badge/…` — never a dynamic build/coverage endpoint, which rots or leaks a private URL. A coverage badge is allowed when the repo has a real, enforced gate; hardcode the number the gate enforces.
- **Every badge must be backed by the tech-stack table**, same version. A badge for something the project does not use is a lie the reader will act on.
- **12–16 badges.** Fewer looks unfinished; more is wallpaper.
- No link wrapping — plain `![alt](url)`, not `[![…](…)](…)`.
- Never a licence badge unless the repo has a `LICENSE` file.

**Order** — runtime first, process last:

1. Runtime / platform (`.NET`, `Node`, `Python`, `Go`, `Java`)
2. Language (`C#`, `TypeScript`)
3. Framework (`Next.js`, `ASP.NET Core`, `FastAPI`, `Spring Boot`)
4. Database + data access (`PostgreSQL`, `EF Core`, `Prisma`, `SQLAlchemy`)
5. Migrations (`Flyway`, `Alembic`)
6. Jobs / queue (`Hangfire`, `BullMQ`, `Celery`)
7. Orchestration (`.NET Aspire`, `Docker`, `Turborepo`)
8. Tests (framework list)
9. Coverage (only if gated)
10. API / contract (`OpenAPI`, `GraphQL`)
11. Auth (`SAML 2.0 SSO`, `OAuth2`, `NextAuth`)
12. Architecture (`Clean Architecture`, `Hexagonal`, `Feature-sliced`)
13. Branching (`GitFlow`, `trunk-based`)
14. Commits (`Conventional`)
15. Hooks (`pre-commit`, `husky`)

## Syntax

```
![Label](https://img.shields.io/badge/<label>-<message>-<colour>?logo=<slug>&logoColor=white)
```

URL-encode inside the badge path: space → `%20`, `#` → `%23`, `/` → `%2F`, `-` → `--`. So `C#-14` → `C%23-14`, `pre-commit` → `pre--commit`, `100% line / branch` → `100%25%20line%20%2F%20branch`.

## Catalogue

Copy-paste, then correct the version.

```markdown
![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?logo=dotnet&logoColor=white)
![C#](https://img.shields.io/badge/C%23-14-239120?logo=csharp&logoColor=white)
![Node](https://img.shields.io/badge/Node-22.x-339933?logo=nodedotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15-000000?logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Java](https://img.shields.io/badge/Java-21-ED8B00?logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.4-6DB33F?logo=springboot&logoColor=white)
![Go](https://img.shields.io/badge/Go-1.23-00ADD8?logo=go&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![EF Core](https://img.shields.io/badge/EF%20Core-10.0-512BD4)
![Prisma](https://img.shields.io/badge/Prisma-6-2D3748?logo=prisma&logoColor=white)
![Flyway](https://img.shields.io/badge/Flyway-12.6-CC0200?logo=flyway&logoColor=white)
![Hangfire](https://img.shields.io/badge/Hangfire-1.8-B4009E)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
![Turborepo](https://img.shields.io/badge/Turborepo-2-EF4444?logo=turborepo&logoColor=white)
![Tests](https://img.shields.io/badge/tests-xUnit%20%2B%20FluentAssertions%20%2B%20Moq-5E5E5E)
![Tests](https://img.shields.io/badge/tests-Vitest%20%2B%20Playwright-5E5E5E)
![Coverage](https://img.shields.io/badge/coverage-100%25%20line%20%2F%20branch-success)
![OpenAPI](https://img.shields.io/badge/API-OpenAPI%203-85EA2D?logo=swagger&logoColor=black)
![Auth](https://img.shields.io/badge/auth-SAML%202.0%20SSO-orange)
![Auth](https://img.shields.io/badge/auth-OAuth2%20client%20credentials-orange)
![Architecture](https://img.shields.io/badge/architecture-Clean%20Architecture-informational)
![GitFlow](https://img.shields.io/badge/branching-GitFlow-05122A)
![Conventional Commits](https://img.shields.io/badge/commits-Conventional-FE5196?logo=conventionalcommits&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-76b900?logo=pre-commit&logoColor=white)
```

For a tech not listed here, use its brand hex and its [simple-icons](https://simpleicons.org) slug as `logo=`. If there is no icon, omit `logo=` entirely rather than guessing a slug — a broken logo renders as a blank gap.
