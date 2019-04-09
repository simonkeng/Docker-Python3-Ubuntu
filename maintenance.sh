#!/usr/bin/env bash

while true
do
    sleep 60
    docker kill $(docker ps -a | grep pdf-extractor | awk '{print $1}')
done
