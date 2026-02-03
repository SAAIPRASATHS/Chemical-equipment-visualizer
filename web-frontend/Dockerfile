FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project
COPY . .

# Build
RUN npm run build

# Serve with a simple server
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
