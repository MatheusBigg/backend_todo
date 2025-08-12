FROM python:3.13-slim

WORKDIR /app

RUN pip install uv uvicorn

COPY pyproject.toml .
COPY uv.lock .

RUN uv pip install --system .

# Copia o restante do código da sua aplicação
COPY . .

EXPOSE 8000

# Comando para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
