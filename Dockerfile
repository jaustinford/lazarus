# syntax=docker/dockerfile:1

ARG BUILD_ARCH

FROM --platform=${BUILD_ARCH} docker:28.0.4-dind-alpine3.21

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
