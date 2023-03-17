#!/bin/bash

PREFIX=""

# Try pipenv
PIPENV_PREFIX="pipenv run"
if [ -z "${PREFIX}" ] && type "pipenv" > /dev/null 2>&1; then
    pipenv --venv > /dev/null 2>&1 && PREFIX=${PIPENV_PREFIX}
fi

# Try conda
CONDA_ENV_FILE="etc/conda-environment.yml"
CONDA_ENV_NAME=""
CONDA_PREFIX="conda run"
if [ -z "${PREFIX}" ] && type "conda" > /dev/null 2>&1; then
    if [ -z ${CONDA_ENV_NAME} ]; then
        CONDA_ENV_NAME=$(head -1 ${CONDA_ENV_FILE} | sed -E 's/^[^:]*:[[:space:]]*//')
    fi
    if [ -n ${CONDA_ENV_NAME} ]; then
        CONDA_PREFIX="${CONDA_PREFIX} -n ${CONDA_ENV_NAME}"
    fi
    conda info -e | grep -q "^${CONDA_ENV_NAME}\s" && PREFIX=${CONDA_PREFIX}
fi
echo $PREFIX
