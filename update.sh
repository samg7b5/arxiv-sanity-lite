#!/bin/bash
docker exec arxiv-sanity python3 arxiv_daemon.py --num 2000
if [ $? -eq 0 ]; then
    echo "New papers detected! Running compute.py"
    docker exec arxiv-sanity python3 compute.py
else
    echo "No new papers were added"
fi
