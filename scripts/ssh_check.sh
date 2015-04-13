#!/bin/bash

if [ $# -ne 4 ]; then
	echo "Usage: $0 [host] [port] [user] [pass]"
	exit 1
fi

## USER CONFIG
# Time limit, in seconds
TIMELIMIT=5

# Command to run remotely
CMD="whoami"

# Expected output
EXPECTED=$3

## END USER CONFIG

HOST=$1
PORT=$2
USER=$3
PASS=$4

COMMAND="sshpass -p '$PASS' ssh -o StrictHostKeyChecking=no -o ConnectTimeout=$TIMELIMIT $USER@$HOST -p $PORT $CMD"
OUTPUT=$(eval $COMMAND 2> /dev/null)

echo "ScoreEngine Module: ssh_check"
echo
echo "RUNNING: $COMMAND"
echo "EXPECTED: $EXPECTED"
echo "OUTPUT: $OUTPUT"

if [ "$OUTPUT" == "$EXPECTED" ]; then
	exit 0;
else
	exit 1;
fi