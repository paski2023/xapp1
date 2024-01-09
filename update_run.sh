#!/bin/bash
sudo docker stop xapp
sudo docker rm xapp
sudo docker build --no-cache -f Dockerfile -t xapp_oai:mrn_base .
sudo docker run -dit --name xapp --net=host xapp_oai:mrn_base
sudo docker exec -it xapp bash