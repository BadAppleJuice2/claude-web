FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code

WORKDIR /app
RUN git clone https://github.com/heng1234/claude-web.git .

RUN python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt

RUN sed -i 's/uvicorn.run(app, host="127.0.0.1", port=port)/host = os.environ.get("HOST", "0.0.0.0")\n    uvicorn.run(app, host=host, port=port)/' server.py

EXPOSE 8765

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
