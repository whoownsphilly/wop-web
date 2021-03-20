#!/bin/sh
POETRY_PATH=`poetry env list --full-path | grep Activated | cut -d' ' -f1` 
POETRY_ACTIVATED=${POETRY_PATH}/bin/activate
echo "Enter the following in your terminal:"
echo source ${POETRY_ACTIVATED}
