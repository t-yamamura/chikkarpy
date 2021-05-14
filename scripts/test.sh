#!/usr/bin/env bash

function copy_dictionary() {
  DIC_TYPE=$1
  if [[ ! -f "../tests/resources/${DIC_TYPE}.dic" ]]; then
    cp ../.travis/"${DIC_TYPE}".dic.test ../tests/resources/"${DIC_TYPE}".dic
  fi
  DIFF=$(diff ../.travis/"${DIC_TYPE}".dic.test ../tests/resources/"${DIC_TYPE}".dic)
  if [[ "$DIFF" != "" ]]; then
      cp ../.travis/"${DIC_TYPE}".dic.test ../tests/resources/"${DIC_TYPE}".dic
  fi
}

echo $(dirname $0)

copy_dictionary "system"
copy_dictionary "user"
copy_dictionary "user2"

# unittest
# shellcheck disable=SC2006
RES=`cd ..; /usr/bin/python3 -m unittest discover tests -p '*test*.py' 2>&1`
# shellcheck disable=SC2006
RES_TAIL=`echo "$RES" | tail -1`
if [[ $RES_TAIL != "OK" ]]; then
    >&2 echo "$RES"
fi