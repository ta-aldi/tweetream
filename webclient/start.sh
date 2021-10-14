#!/bin/bash

docker build -t webclient:multistage .
docker run -d -p 80:8080 webclient:multistage
