# syntax=docker/dockerfile:1

FROM --platform=linux/arm64 docker:28.0.4-dind-alpine3.21

RUN \
    apk add \
        bash \
        python3 \
        apcupsd

WORKDIR /lazarus

COPY --chmod=755 \
    src/ ./src/

COPY conf/ups-0.conf /etc/apcupsd/ups-0.conf
COPY conf/ups-1.conf /etc/apcupsd/ups-1.conf
