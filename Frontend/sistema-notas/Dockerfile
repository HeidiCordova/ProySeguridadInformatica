# Fase 1: Construcción
FROM node:18 AS build
WORKDIR /app

# Copiar package.json y package-lock.json para instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar el resto del código fuente
COPY . .

# Construir la aplicación Angular en modo producción
RUN npx ng build --configuration=production

# Fase 2: Servir con NGINX
FROM nginx:alpine

# Copiar la configuración de NGINX
COPY default.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos generados en la fase de construcción al contenedor NGINX
COPY --from=build /app/dist/sistema-notas/browser /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

# Comando para iniciar NGINX
CMD ["nginx", "-g", "daemon off;"]
