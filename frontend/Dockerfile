# =========================
# Stage 1: Build React/Vite
# =========================
FROM node:22-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build


# =========================
# Stage 2: Nginx runtime
# =========================
FROM nginx:1.27-alpine AS runtime

RUN apk add --no-cache curl \
    && rm -f /etc/nginx/conf.d/default.conf \
    && touch /run/nginx.pid \
    && chown -R nginx:nginx \
        /run/nginx.pid \
        /var/cache/nginx \
        /usr/share/nginx/html \
        /etc/nginx/conf.d

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

RUN chown -R nginx:nginx \
    /usr/share/nginx/html \
    /etc/nginx/conf.d

USER nginx

EXPOSE 8080

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD curl --fail --silent http://localhost:8080/healthz || exit 1

CMD ["nginx", "-g", "daemon off;"]