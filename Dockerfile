FROM ghcr.io/astral-sh/uv:0.11.6-python3.12-trixie

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    cmake \
    make \
    libolm-dev \
    librocksdb-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Синкаем проект
RUN uv sync

EXPOSE 8000

RUN mkdir -p /app/data

CMD ["uv", "run", "python", "-m", "src.mxuserbot"]