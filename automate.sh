#!/bin/bash

git pull origin main
sudo docker-compose -f production.yml down
sudo docker-compose -f production.yml build
sudo docker-compose -f production.yml up -d
