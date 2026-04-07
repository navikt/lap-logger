FROM python:3.14-slim

WORKDIR /app

ENV UV_CACHE_DIR=/tmp/uv-cache

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

COPY . .

EXPOSE 8080

CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]

