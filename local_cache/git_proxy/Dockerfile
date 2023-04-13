FROM node

COPY git-cache-http-server /git-cache-http-server

WORKDIR /git-cache-http-server
RUN npm install && npm run build

EXPOSE 80
VOLUME ["/git-cache-http-server/data"]
CMD ["/git-cache-http-server/bin/git-cache-http-server", "-p", "80", "-c", "/git-cache-http-server/data"]
