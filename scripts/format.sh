#!/usr/bin/env bash

flake8 --show --config=flake8.cfg ../setup.py ../chikkarpy ../tests >> .log 2>&1

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
        echo "invalid license header on ${FILE}" >> scripts/.log 2>&1
    fi
done

cat scripts/.log
ERROR_LINE_NUM=$(cat scripts/.log | wc -l)
rm scripts/.log

if [ "${ERROR_LINE_NUM}" -gt 0 ]; then
  exit 1
fi
