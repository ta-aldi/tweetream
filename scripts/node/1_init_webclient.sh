#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)

sudo apt-get install -y git librdkafka-dev golang-go build-essential

# 1. create webclient service file
WEBSERVICE=/etc/systemd/system/webclient.service
TWEETREAM=/home/michael/tweetream
if [ -f $WEBSERVICE ]; then
    echo "$WEBSERVICE found."
else
    touch $WEBSERVICE

    echo "[Unit]" >> $WEBSERVICE
    echo "Description=Webclient Service" >> $WEBSERVICE
    echo "Requires=network.target" >> $WEBSERVICE
    echo "After=network.target" >> $WEBSERVICE
    echo "" >> $WEBSERVICE

    echo "[Service]" >> $WEBSERVICE
    echo "Type=simple" >> $WEBSERVICE
    echo "ExecStart=cd $TWEETREAM/webclient && go mod vendor && make go_run_web" >> $WEBSERVICE
    echo "TimeoutSec=30" >> $WEBSERVICE
    echo "Restart=on-failure" >> $WEBSERVICE
    echo "" >> $WEBSERVICE

    echo "[Install]" >> $WEBSERVICE
    echo "WantedBy=default.target" >> $WEBSERVICE

    echo "$WEBSERVICE created."
fi
sudo systemctl start webclient
sudo systemctl enable webclient
