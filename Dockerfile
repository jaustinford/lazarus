# syntax=docker/dockerfile:1

FROM docker:28.0.4-dind-alpine3.21

RUN \
    apk add \
        bash \
        python3

WORKDIR /lazarus

COPY --chmod=755 \
    src/ ./src/
