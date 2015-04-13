#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [host]"
	exit 1
fi

## USER CONFIG
# Time limit, in seconds
TIMELIMIT=5

## END USER CONFIG

HOST=$1

COMMAND="ping -c 1 -t $TIMELIMIT $HOST"
OUTPUT=$(eval $COMMAND)

echo "ScoreEngine Module: icmp_check"
echo
echo "RUNNING: $COMMAND"
echo "EXPECTED: 1 packet received"
echo "OUTPUT:"
echo "$OUTPUT"

if [ $? == 0 ]; then
	exit 0;
else
	exit 1;
fi