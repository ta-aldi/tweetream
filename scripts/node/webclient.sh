#!/bin/bash

TWEETREAM=/home/michael/tweetream

cd $TWEETREAM/webclient
go mod vendor
make go_run_web
