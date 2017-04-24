#!/bin/bash

# set the script to exit on any failure
set -e

sudo apt-get update -y
sudo apt-get install python-pip -y
sudo pip install requests
sudo apt-get install tshark -y
sudo apt-get install xdotool -y
sudo pip install selenium
sudo apt-get install firefox -y
