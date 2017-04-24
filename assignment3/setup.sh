#!/bin/bash
set -e

mkdir -p database
mkdir -p crawler/logs
mkdir -p exploit_scripts
ln -s verifier/geckodriver exploit_scripts/geckodriver
ln -s verifier/sniffer.py exploit_scripts/sniffer.py

sudo apt-get update

sudo apt-get install python-pip -y
sudo apt-get install firefox -y
sudo apt-get install sqlite3 -y
sudo apt-get install TShark -y
sudo apt-get install mitmproxy -y

sudo pip install pyshark
sudo pip install requests
sudo pip install selenium
sudo pip install sqlalchemy
sudo pip install scrapy
sudo pip install loginform
sudo pip install scapy
