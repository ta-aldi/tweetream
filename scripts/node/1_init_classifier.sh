#!/bin/bash
# Created by Michael Susanto (@michaelsusanto81)

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
    echo "ExecStart=pip3 install -r $TWEETREAM/modules/requirements.txt && python3 $TWEETREAM/modules/classifier.py" >> $CLSSFRSERVICE
    echo "TimeoutSec=30" >> $CLSSFRSERVICE
    echo "Restart=on-failure" >> $CLSSFRSERVICE
    echo "" >> $CLSSFRSERVICE

    echo "[Install]" >> $CLSSFRSERVICE
    echo "WantedBy=default.target" >> $CLSSFRSERVICE

    echo "$CLSSFRSERVICE created."
fi
sudo systemctl start classifier
sudo systemctl enable classifier
