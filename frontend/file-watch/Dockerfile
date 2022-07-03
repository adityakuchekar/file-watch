#stage 1
FROM node:latest as node
WORKDIR /frontend-app
COPY . .
RUN npm install -g @angular/cli
RUN npm install
CMD [ "ng", "serve", "--host", "0.0.0.0"]