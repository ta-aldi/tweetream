#!/bin/bash

# docker build -t webclient:multistage .
docker build -t webclient .
docker run -d --network host webclient
