# syntax=docker/dockerfile:1

FROM python:3.9.19-bookworm

RUN \
    curl https://download.docker.com/linux/debian/gpg \
        --output /etc/apt/keyrings/docker.asc

RUN \
    cat <<EOF > /etc/apt/sources.list.d/docker.list
deb [signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian/ bookworm stable
EOF

RUN \
    apt update -y && \
    apt install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin    

RUN \
    apt install -y \
        apcupsd

RUN \
    pip install \
        apcaccess

WORKDIR /lazarus

COPY --chmod=755 \
    src/ ./src/

COPY --chmod=644 \
    conf/ ./conf/
