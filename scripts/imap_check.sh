#!/bin/bash

if [ $# -ne 5 ]; then
	echo "Usage: $0 [host] [port] [domain] [user] [pass]"
	exit 1
fi

## USER CONFIG
# Time limit, in seconds
TIMELIMIT=5

# Period between netcat sends command
NC_WAIT=1

## END USER CONFIG

EXPECTED="a1 OK LOGIN completed."

HOST=$1
PORT=$2
DOMAIN=$3
USER=$4
PASS=$5

COMMAND="echo -ne 'a1 LOGIN $DOMAIN\\$USER $PASS\r\na5 LOGOUT\r\n' | nc -i $NC_WAIT -w $TIMELIMIT $HOST $PORT"
OUTPUT=$(eval $COMMAND)

# Split by line
ACTUAL=$(echo "$OUTPUT" | sed -n 2p | tr -d '\r')

echo "ScoreEngine Module: imap_check"
echo
echo "RUNNING: $COMMAND"
echo "EXPECTED: $EXPECTED"
echo "ACTUAL: $ACTUAL"
echo
echo "OUTPUT:"
echo "$OUTPUT"

if [ "$ACTUAL" == "$EXPECTED" ]; then
	exit 0;
else
	exit 1;
fi