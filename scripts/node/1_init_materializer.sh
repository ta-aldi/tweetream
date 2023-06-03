#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)
# Adjusted by Aldi Naufal Fitrah

sudo apt-get install -y python3-pip python3-dev librdkafka-dev

# 1. create materializer service file
MTRLZSERVICE=/etc/systemd/system/materializer.service
TWEETREAM=/home/aldi_naufal/tweetream
rm -rf 
if [ -f $MTRLZSERVICE ]; then
    echo "$MTRLZSERVICE found."
else
    sudo cat << EOF | sudo tee $MTRLZSERVICE
[Unit]
Description=Materializer Service
Requires=network.target
After=network.target

[Service]
Type=simple
ExecStart=bash $TWEETREAM/scripts/node/materializer.sh

[Install]
WantedBy=default.target
EOF
fi
sudo systemctl start materializer
sudo systemctl enable materializer
