FROM node:20-alpine AS frontend

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build && rm -rf node_modules

FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache libstdc++ wget unzip nginx

RUN mkdir -p /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/log/nginx

COPY --from=frontend /app/frontend/dist /var/www/html

RUN wget -q "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip" -O /tmp/android-sdk.zip && \
    unzip -q /tmp/android-sdk.zip -d /opt/android-sdk && \
    rm /tmp/android-sdk.zip && \
    mkdir -p /opt/android-sdk/cmdline-tools/latest && \
    mv /opt/android-sdk/cmdline-tools /opt/android-sdk/cmdline-tools.bak 2>/dev/null || true && \
    mv /opt/android-sdk/cmdline-tools.bak/* /opt/android-sdk/cmdline-tools/latest/ 2>/dev/null || true && \
    rm -rf /opt/android-sdk/cmdline-tools.bak

ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=${PATH}:${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools

RUN yes | ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin/sdkmanager --licenses 2>/dev/null || true
RUN ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin/sdkmanager "platform-tools" "build-tools;34.0.0" 2>/dev/null || true

COPY pyproject.toml uv.lock* ./
RUN pip install --no-cache-dir uv && \
    uv pip install --system -r pyproject.toml

COPY app/ ./app/
COPY scripts/ ./scripts/

RUN cat > /etc/nginx/http.d/default.conf << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /static {
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

CMD ["sh", "-c", "uvicorn app.main:app --host 127.0.0.1 --port 8000 & nginx -g 'daemon off;'"]
