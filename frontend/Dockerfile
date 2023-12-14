# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
# COPY ./nginx.conf /etc/nginx/conf.d/default.conf
# COPY ./server.key /etc/ssl
# COPY ./server.key /etc/ssl/
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
# EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]