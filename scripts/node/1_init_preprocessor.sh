#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)
# Adjusted by Aldi Naufal Fitrah

sudo apt-get install -y python3-pip python3-dev librdkafka-dev

# 1. create preprocessor service file
PREPRCSRSERVICE=/etc/systemd/system/preprocessor.service
TWEETREAM=/home/$USER/tweetream
if [ -f $PREPRCSRSERVICE ]; then
    echo "$PREPRCSRSERVICE found."
else
    touch $PREPRCSRSERVICE

    echo "[Unit]" >> $PREPRCSRSERVICE
    echo "Description=Preprocessor Service" >> $PREPRCSRSERVICE
    echo "Requires=network.target" >> $PREPRCSRSERVICE
    echo "After=network.target" >> $PREPRCSRSERVICE
    echo "" >> $PREPRCSRSERVICE

    echo "[Service]" >> $PREPRCSRSERVICE
    echo "Type=simple" >> $PREPRCSRSERVICE
    echo "ExecStart=bash $TWEETREAM/scripts/node/preprocessor.sh" >> $PREPRCSRSERVICE
    echo "" >> $PREPRCSRSERVICE

    echo "[Install]" >> $PREPRCSRSERVICE
    echo "WantedBy=default.target" >> $PREPRCSRSERVICE

    echo "$PREPRCSRSERVICE created."
fi
sudo systemctl start preprocessor
sudo systemctl enable preprocessor
