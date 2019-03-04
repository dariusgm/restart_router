FROM alpine:3.7
RUN apk add --no-cache chromium
ENTRYPOINT ["chromium-browser", "--headless", "--disable-gpu", "--disable-software-rasterizer", "--disable-dev-shm-usage", "--remote-debugging-port=9222", "--remote-debugging-address=0.0.0.0"]