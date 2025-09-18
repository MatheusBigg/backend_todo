# Todo App

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)  
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal?logo=fastapi)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)  
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker&logoColor=white)  
![License](https://img.shields.io/badge/license-MIT-green)  

**Backend Todo App** é um projeto de estudo de uma API robusta para gerenciamento de tarefas buscando as melhores práticas do ecossistema Python.

---

## Funcionalidades

- **Gerenciamento de Tarefas**: Crie, visualize, atualize e delete tarefas.  
- **Autenticação**: Rotas seguras com autenticação de usuário via JWT.  
- **Modelo de Dados**: Entidades de **Usuário** e **Tarefa** com estados definidos:
  - `draft`
  - `todo`
  - `doing`
  - `done`
  - `trash`

---

## Tecnologias Principais

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)  
- **Gerenciamento de Dependências**: [uv](https://github.com/astral-sh/uv)  
- **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/) com [SQLAlchemy](https://www.sqlalchemy.org/)  
- **Migrações**: [Alembic](https://alembic.sqlalchemy.org/)  
- **Testes**: [pytest](https://docs.pytest.org/)  
- **Qualidade de Código**: [ruff](https://github.com/astral-sh/ruff)  
- **Ambiente**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)  
- **CI/CD**: [GitHub Actions](https://docs.github.com/actions)  

---

## ⚙️ Como Usar

### 1. Clone o repositório
```bash
git clone https://github.com/MatheusBigg/backend_todo.git
cd backend_todo
```

### 2. Inicie o projeto com Docker Compose
```bash
docker-compose up --build
```

### 3. Acesse a Docs Interativo
    Swagger UI: http://localhost:8000/docs
    Redoc: http://localhost:8000/redoc

### 4. Execute os testes
```bash
docker-compose exec app uv run task test
```

## Observação

Este projeto é um estudo e demonstração de boas práticas no desenvolvimento de APIs com Python e FastAPI