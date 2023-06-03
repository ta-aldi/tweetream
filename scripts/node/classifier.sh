#!/bin/bash

TWEETREAM=/home/$USER/tweetream

cd $TWEETREAM
pip3 install -r modules/requirements.txt
python3 modules/classifier.py
