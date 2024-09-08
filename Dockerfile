FROM node:20-slim AS builder
RUN mkdir /src
COPY . /src/
WORKDIR /src
RUN npm install
RUN npm run test -- --watchAll=false
RUN npm run build

FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=builder /src/build ./
