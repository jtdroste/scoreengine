#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 [host] [port]"
	exit 1
fi

## USER CONFIG
# Time limit, in seconds
TIMELIMIT=5

# Item to search for
SEARCH_STRING="Your one shop stop for everything Windows!"

# Output
SEARCH_EXPECTED="2"

## END USER CONFIG

HOST=$1
PORT=$2

COMMAND="curl -sLk --max-time $TIMELIMIT 'https://$HOST:$PORT/wordpress' | grep -c '<hidden>'"
REAL_COMMAND=$(echo $COMMAND | sed "s/<hidden>/${SEARCH_STRING}/g")
OUTPUT=$(eval $REAL_COMMAND)

echo "ScoreEngine Module: https-content"
echo
echo "RUNNING: $COMMAND"
echo "EXPECTED: $SEARCH_EXPECTED"
echo "OUTPUT: $OUTPUT"

if [ $OUTPUT -eq $SEARCH_EXPECTED ]; then
	exit 0;
else
	exit 1;
fi