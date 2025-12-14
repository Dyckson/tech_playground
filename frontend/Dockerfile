# ====================
# Stage 1: Builder
# ====================
FROM node:20-alpine AS builder

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile || pnpm install

# Copy source code
COPY . .

# Build arguments
ARG VITE_API_URL=http://localhost:9876
ENV VITE_API_URL=$VITE_API_URL

# Build application
RUN pnpm run build

# ====================
# Stage 2: Production with Distroless
# ====================
FROM gcr.io/distroless/nodejs20-debian12

# Set working directory
WORKDIR /app

# Copy built assets from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Create simple server file
COPY --from=builder /app/server.js ./

# Expose port
EXPOSE 3000

# Run application
CMD ["server.js"]
