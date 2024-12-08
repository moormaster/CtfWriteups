#!/bin/bash
# vi: et ts=2

PARAM_IS_LOCAL=0
PARAM_IP=""
PARAM_PORT=""

parse_arguments() {
  if [ $# -eq 0 ]
  then
    echo "no arguments given $#" 2>&1
    print_usage
    exit 1
  fi

  while [ $# -gt 0 ]
  do
    case $1 in
      --local)
        PARAM_IS_LOCAL=1
        shift
        ;;

      *)
        if [ "${#PARAM_IP}" -eq 0 ]
        then
          PARAM_IP=$1
        elif [ "${#PARAM_PORT}" -eq 0 ]
        then
          PARAM_PORT=$1
        elif [ ${PARAM_IS_LOCAL} -eq 0 ]
        then
          echo "invalid parameter: $1" 1>&2
          print_usage
          exit 1
        fi
        shift
        ;;
    esac
  done
}

print_usage() {
  echo "usage: $0 (<ip> <port> | --local)" 1>&2
}

parse_arguments "$@"

mkfifo nc_channel
mkfifo py_channel

if [ ${PARAM_IS_LOCAL} -eq 0 ]
then 
  cat py_channel | nc $1 $2 >> nc_channel &
else
  cat py_channel | python chall.py >> nc_channel &
fi

cat nc_channel | python numbers2.py >> py_channel
 
