#!/bin/bash
APP_NAME=$1
APP_PORT=$2

MEMORY="2g"
SWAP_MEMORY="1g"
CPUS="4"

docker kill "${APP_NAME}" || true
docker rm -f "${APP_NAME}" || true

docker run -d --cpus="${CPUS}" --memory="${MEMORY}" --memory-swap="${SWAP_MEMORY}" --name "${APP_NAME}" -p "${APP_PORT}:3838" "${APP_NAME}"
docker update --restart always "${APP_NAME}"
