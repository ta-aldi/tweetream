#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)
# Adjusted by Aldi Naufal Fitrah

sudo apt-get install -y python3-pip python3-dev librdkafka-dev

# 1. create classifier service file
CLSSFRSERVICE=/etc/systemd/system/classifier.service
TWEETREAM=/home/$USER/tweetream
rm -rf $CLSSFRSERVICE
if [ -f $CLSSFRSERVICE ]; then
    echo "$CLSSFRSERVICE found."
else
    sudo cat << EOF | sudo tee $CLSSFRSERVICE
[Unit]
Description=Classifier Service
Requires=network.target
After=network.target

[Service]
Type=simple
ExecStart=bash $TWEETREAM/scripts/node/classifier.sh

[Install]
WantedBy=default.target
EOF

    echo "$CLSSFRSERVICE created."
fi
sudo systemctl start classifier
sudo systemctl enable classifier
