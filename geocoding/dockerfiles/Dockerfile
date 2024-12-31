FROM node:16.13.2-alpine

WORKDIR /app
ADD package.json package.json
ADD package-lock.json package-lock.json
ADD index.js index.js

RUN npm install

CMD node index.js
