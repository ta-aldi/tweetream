#!/bin/bash

TWEETREAM=/home/michael/tweetream

cd $TWEETREAM
pip3 install -r modules/requirements.txt
python3 modules/classifier.py
