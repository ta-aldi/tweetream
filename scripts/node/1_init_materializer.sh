#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)
# Adjusted by Aldi Naufal Fitrah

sudo apt-get install -y python3-pip python3-dev librdkafka-dev

# 1. create materializer service file
MTRLZSERVICE=/etc/systemd/system/materializer.service
TWEETREAM=/home/$USER/tweetream
if [ -f $MTRLZSERVICE ]; then
    echo "$MTRLZSERVICE found."
else
    touch $MTRLZSERVICE

    echo "[Unit]" >> $MTRLZSERVICE
    echo "Description=Materializer Service" >> $MTRLZSERVICE
    echo "Requires=network.target" >> $MTRLZSERVICE
    echo "After=network.target" >> $MTRLZSERVICE
    echo "" >> $MTRLZSERVICE

    echo "[Service]" >> $MTRLZSERVICE
    echo "Type=simple" >> $MTRLZSERVICE
    echo "ExecStart=bash $TWEETREAM/scripts/node/materializer.sh" >> $MTRLZSERVICE
    echo "" >> $MTRLZSERVICE

    echo "[Install]" >> $MTRLZSERVICE
    echo "WantedBy=default.target" >> $MTRLZSERVICE

    echo "$MTRLZSERVICE created."
fi
sudo systemctl start materializer
sudo systemctl enable materializer
