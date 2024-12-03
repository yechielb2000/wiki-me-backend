FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /

COPY /app /app

COPY pyproject.toml /

COPY uv.lock /

RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0"]
