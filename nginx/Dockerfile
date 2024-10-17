FROM nginx:latest

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf
COPY certs /etc

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]