FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive \
    GLAMA_VERSION="0.2.0" \
    PATH="/home/service-user/.local/bin:${PATH}"

# Create user and directories
RUN groupadd -r service-user && \
    useradd -u 1987 -r -m -g service-user service-user && \
    mkdir -p /home/service-user/.local/bin /app && \
    chown -R service-user:service-user /home/service-user /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl wget git build-essential software-properties-common \
    libssl-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 22 and package managers
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g mcp-proxy@2.10.6 pnpm@9.15.5 bun@1.1.42 && \
    node --version

# Install uv and Python 3.13
RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR="/usr/local/bin" sh && \
    uv python install 3.13 --default --preview && \
    ln -s $(uv python find) /usr/local/bin/python && \
    python --version

# Switch to non-root user
USER service-user
WORKDIR /app

# Clone your repo and switch to pinned commit
RUN git clone https://github.com/rmtech1/txtai-assistant-mcp . && \
    git checkout 06f4ecc6c0d18f2fc6d632903bba2dcc77eab71f

# Make your start.sh executable
RUN chmod +x ./scripts/dockerstart.sh

# Build the frontend/backend if needed
RUN pnpm install && pnpm run build

# Install Python server requirements
RUN pip install --upgrade pip && pip install -r server/requirements.txt

# Default CMD
CMD ["bash", "./scripts/dockerstart.sh"]