#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)
# Adjusted by Aldi Naufal Fitrah

sudo apt-get install -y python3-pip python3-dev librdkafka-dev

# 1. create classifier service file
CLSSFRSERVICE=/etc/systemd/system/classifier.service
TWEETREAM=/home/$USER/tweetream
if [ -f $CLSSFRSERVICE ]; then
    echo "$CLSSFRSERVICE found."
else
    touch $CLSSFRSERVICE

    echo "[Unit]" >> $CLSSFRSERVICE
    echo "Description=Classifier Service" >> $CLSSFRSERVICE
    echo "Requires=network.target" >> $CLSSFRSERVICE
    echo "After=network.target" >> $CLSSFRSERVICE
    echo "" >> $CLSSFRSERVICE

    echo "[Service]" >> $CLSSFRSERVICE
    echo "Type=simple" >> $CLSSFRSERVICE
    echo "ExecStart=bash $TWEETREAM/scripts/node/classifier.sh" >> $CLSSFRSERVICE
    echo "" >> $CLSSFRSERVICE

    echo "[Install]" >> $CLSSFRSERVICE
    echo "WantedBy=default.target" >> $CLSSFRSERVICE

    echo "$CLSSFRSERVICE created."
fi
sudo systemctl start classifier
sudo systemctl enable classifier
