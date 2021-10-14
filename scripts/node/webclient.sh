#!/bin/bash

TWEETREAM=/home/michael/go/src/github.com/michaelsusanto81/tweetream

cd $TWEETREAM/webclient
go mod vendor
make go_run_web
