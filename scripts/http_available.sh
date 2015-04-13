#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 [host] [port]"
	exit 1
fi

## USER CONFIG
# Time limit, in seconds
TIMELIMIT=5

## END USER CONFIG

HOST=$1
PORT=$2
COMMAND="curl -sL --max-time $TIMELIMIT -w %{http_code} 'http://$HOST:$PORT/wordpress' -o /dev/null"
OUTPUT=$(eval $COMMAND)

echo "ScoreEngine Module: http-available"
echo
echo "RUNNING: $COMMAND"
echo "EXPECTED: 200"
echo "OUTPUT: $OUTPUT"

if [ $OUTPUT == 200 ]; then
	exit 0;
else
	exit 1;
fi