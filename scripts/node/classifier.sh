#!/bin/bash

TWEETREAM=/home/aldi_naufal/tweetream

cd $TWEETREAM
pip3 install -r modules/requirements.txt
python3 modules/classifier.py
