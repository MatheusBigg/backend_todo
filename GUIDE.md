
# Guia Detalhado: Como Construir o Todo App

## Sumário
- [Inicialização do Projeto](#inicialização-do-projeto)
- [Configuração do Projeto e Dependências](#configuração-do-projeto-e-dependências)
- [Banco de Dados e Modelos](#banco-de-dados-e-modelos)
- [Segurança e Autenticação](#segurança-e-autenticação)
- [Rotas da API e Lógica de Negócio](#rotas-da-api-e-lógica-de-negócio)
- [Schemas com Pydantic](#schemas-com-pydantic)
- [Execução e Containerização com Docker](#execução-e-containerização-com-docker)
- [Boas práticas rápidas](#boas-práticas-rápidas)

---

## Inicialização do Projeto

### Setup básico e criação de diretório
Crie a pasta do projeto e entre nela:

```bash
mkdir todo_app
cd todo_app
```

### Instalar o `uv`
Instale o gerenciador de dependências `uv` via `pipx` (recomendado) para manter o ambiente limpo:

```bash
pipx install uv
```

### Criar `pyproject.toml`
Crie um `pyproject.toml` básico (ou copie o seu). Exemplo mínimo:

```toml
[project]
name = "todo_app"
version = "0.1.0"
description = "Todo App API"

[project.dependencies]
python = ">=3.11"
fastapi = "^0.95.0"
sqlalchemy = "^2.0"
psycopg = {extras = ["binary"], version = "^3.1"}
alembic = "^1.13"
pydantic = "^2.0"
uvicorn = "^0.23.0"
pwdlib = {extras = ["argon2"], version = "*"}
pyjwt = "^2.8.0"
```

### Sincronizar dependências com `uv`
Depois que o `pyproject.toml` estiver pronto, instale tudo:

```bash
uv sync --dev
```

---

## Configuração do Projeto e Dependências

- Estruture o projeto com diretórios como `app/`, `app/api/`, `app/core/`, `app/models/`, `app/schemas/`, `app/db/`, `tests/`.
- Mantenha variáveis sensíveis em um `.env` (ex: `DATABASE_URL`, `SECRET_KEY`).

---

## Banco de Dados e Modelos

### Conexão (ex.: `app/db/database.py`)
- Use `create_async_engine` do SQLAlchemy para conexão assíncrona.
- Crie uma fábrica de sessões (`get_session`) usada como dependência no FastAPI para abrir/fechar sessões automaticamente.

### Modelos (ex.: `app/models/models.py`)
- **User**: `username`, `email`, `password` (hash), relacionamento com `Todo`.
- **Todo**: `title`, `description`, `state` (`draft|todo|doing|done|trash`), `user_id` (FK).

---

## Segurança e Autenticação

### Arquivo core (ex.: `app/core/security.py`)
- Hash de senha: use `pwdlib` (ou `passlib`) para criar/verificar hashes seguros.
- JWT: `create_access_token` e validação de token; utilize `SECRET_KEY` e `exp` para expiração.
- `OAuth2PasswordBearer` em `oauth2_scheme` para extrair o token do header e usar em `get_current_user`.

### Rotas de Auth (ex.: `app/api/v1/routers/auth.py`)
- `POST /token` — recebe email (username) e senha e retorna `access_token` se válido.
- `POST /refresh_token` — gera novo token a partir de um token válido (refresh flow simples).

---

## Rotas da API e Lógica de Negócio

### Usuários (`app/api/v1/routers/users.py`)
- `POST /users/` — cria um usuário (valida duplicidade por username/email, salva senha como hash).
- `GET /users/` — lista usuários (rota protegida).
- `PUT /users/{user_id}` — atualiza usuário autenticado (verifica propriedade).
- `DELETE /users/{user_id}` — remove usuário (verifica propriedade).

### Tarefas (`app/api/v1/routers/todos.py`)
- `POST /todos/` — cria tarefa vinculada ao usuário logado (usa `user.id`).
- `GET /todos/` — lista tarefas com filtros por `title`, `description` e `state`.
- `PATCH /todos/{todo_id}` — atualiza tarefa (verifica propriedade).
- `DELETE /todos/{todo_id}` — deleta tarefa (verifica propriedade).

---

## Schemas com Pydantic

- Coloque os schemas em `app/schemas/schemas.py`.
- **Validação**: `UserSchema`, `TodoSchema` — definem campos esperados nas requisições.
- **Resposta**: `UserPublic`, `TodoPublic` — definem o que é retornado (ocultar senha).

Exemplo rápido:

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class TodoSchema(BaseModel):
    title: str
    description: Optional[str]
    state: str  # validar com Enum em implementação

class TodoPublic(TodoSchema):
    id: int
    user_id: int

    class Config:
        orm_mode = True
```

---

## Execução e Containerização com Docker

### Dockerfile (exemplo)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install uv && uv sync --non-interactive

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### Entrypoint (ex.: `entrypoint.sh`)
```bash
#!/bin/sh
uv run alembic upgrade head
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Torne executável:
```bash
chmod +x entrypoint.sh
```

### docker-compose.yaml (exemplo)
```yaml
version: "3.8"
services:
  app:
    build: .
    entrypoint: ./entrypoint.sh
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://app_user:app_password@db:5432/app_db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=app_user
      - POSTGRES_PASSWORD=app_password
      - POSTGRES_DB=app_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

### Rodar a aplicação
```bash
docker-compose up --build
```

A documentação interativa ficará disponível:
- Swagger UI → `http://localhost:8000/docs`
- Redoc → `http://localhost:8000/redoc`

---

## Boas práticas rápidas

- Use `.env` para segredos e não comite-o.
- Tenha scripts de lint/format (ex.: `ruff`, `black`).
- Automatize migrações (alembic) no entrypoint para dev/prod controlado.
- Testes: unitários + integração (use `testcontainers` para PostgreSQL em CI).
- Segurança: HTTPS em produção, rotação de chaves, limite de tentativas de login.

---

## Observações finais
Agradecimentos ao Dunossauro pelas aulas:
https://fastapidozero.dunossauro.com/4.0/