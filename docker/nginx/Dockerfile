# nginxのセットアップ
FROM nginx:alpine

ARG PRODUCTION
ENV HAMCAM_PRODUCTION $PRODUCTION

RUN apk --no-cache add tzdata
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /app
