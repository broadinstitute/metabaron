#!/bin/bash
set -e
cmd="$@"

echo "waiting for db"
sleep 30

exec $cmd