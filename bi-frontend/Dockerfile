# Build stage
FROM node:18 as build

WORKDIR /app

# Copy package files from the correct location
COPY ./bi-frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code from the correct location
COPY ./bi-frontend/ .

# Build the app with environment variables
ARG REACT_APP_FLASK_URL
ENV REACT_APP_FLASK_URL=$REACT_APP_FLASK_URL
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY ./bi-frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
