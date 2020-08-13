# Vueで作ったフロントをビルド
FROM node:alpine as build-stage

ARG PRODUCTION
ENV HAMCAM_PRODUCTION $PRODUCTION

WORKDIR /app
COPY ./hamcam-views/package*.json ./
RUN npm install
COPY ./hamcam-views/ /app/
RUN npm run build

# nginxのセットアップ
FROM nginx:alpine as production-stage

ARG PRODUCTION
ENV HAMCAM_PRODUCTION $PRODUCTION

WORKDIR /app
RUN apk --no-cache add tzdata
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./docker/hamcam-views/nginx.conf /etc/nginx/nginx.conf
