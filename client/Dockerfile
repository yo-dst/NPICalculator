FROM node:lts

RUN npm install -g serve

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY ./ ./

ARG REACT_APP_HOST
ENV REACT_APP_HOST=$REACT_APP_HOST

RUN npm run build

CMD [ "serve", "-s", "build", "-l", "3000" ]
