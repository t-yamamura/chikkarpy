#!/usr/bin/env bash

flake8 --show --config=flake8.cfg ../chikkarpy
flake8 --show --config=flake8.cfg ../tests

HEADER=$(cat license-header.txt)

cd ..

array=()

for FILE in $(find ./chikkarpy -type f -name "*.py"); do
    array+=( ${FILE} )
done

for FILE in $(find ./tests -type f -name "*.py"); do
    array+=( ${FILE} )
done

array+=( ./setup.py )

for FILE in ${array[@]}; do
    FILE_CONTENTS=$(cat "${FILE}")
    if [[ ${FILE_CONTENTS} != ${HEADER}* ]]; then
        >&2 echo "invalid license header on ${FILE}"
    fi
done
