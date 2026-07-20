# Hermes web (Next.js) image. Multi-stage: install deps, build, run.
FROM node:20-slim AS deps
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY apps/web/package.json ./apps/web/package.json
RUN pnpm install --filter @hermes/web...

FROM node:20-slim AS build
WORKDIR /app
RUN corepack enable
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/web/node_modules ./apps/web/node_modules
COPY package.json pnpm-workspace.yaml ./
COPY apps/web ./apps/web
RUN pnpm --filter @hermes/web build

FROM node:20-slim AS run
WORKDIR /app/apps/web
ENV NODE_ENV=production
RUN corepack enable
COPY --from=build /app/apps/web ./
COPY --from=build /app/node_modules /app/node_modules

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
    CMD node -e "fetch('http://localhost:3000/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["pnpm", "start"]
