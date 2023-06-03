#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)
# Adjusted by Aldi Naufal Fitrah

sudo apt-get install -y python3-pip python3-dev librdkafka-dev

# 1. create preprocessor service file
PREPRCSRSERVICE=/etc/systemd/system/preprocessor.service
TWEETREAM=/home/$USER/tweetream
rm -rf $PREPRCSRSERVICE
if [ -f $PREPRCSRSERVICE ]; then
    echo "$PREPRCSRSERVICE found."
else
    sudo cat << EOF | sudo tee $PREPRCSRSERVICE
[Unit]
Description=Preprocessor Service
Requires=network.target
After=network.target

[Service]
Type=simple
ExecStart=bash $TWEETREAM/scripts/node/preprocessor.sh

[Install]
WantedBy=default.target
EOF

    echo "$PREPRCSRSERVICE created."
fi
sudo systemctl start preprocessor
sudo systemctl enable preprocessor
