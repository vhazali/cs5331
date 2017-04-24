#!/bin/bash
set -e
dt=$(date '+%d%m%y%H%M%S');
prefix='crawler/logs/'
suffix='.log'
filename=$prefix$dt$suffix
echo 'Beginning crawl. Logs will be redirected to '$filename
scrapy crawl benchmarks --logfile $filename
echo 'Crawl completed.'
