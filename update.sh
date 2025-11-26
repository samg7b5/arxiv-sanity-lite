#!/bin/bash
docker exec arxiv-sanity python3 arxiv_daemon.py --num 2000
if [ $? -eq 0 ]; then
    echo "New papers detected! Running compute.py"
    docker exec arxiv-sanity python3 compute.py --num 5000 --min_df 6 --max_df 0.15 --max_docs 7000
else
    echo "No new papers were added"
fi

/home/sam/notify/main.sh "📄 arxiv update completed."
