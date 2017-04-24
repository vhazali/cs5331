# This is the main python file where everything starts.
# Combine all components into this file.
# To run: sudo python cookie_monster.py

import time
import requests
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Links
from scanner.scanner import *
from multiprocessing.dummy import Pool

pool = Pool(20)

engine = create_engine('sqlite:///database/scrapedsites.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

# Get all URLs from DB
list_of_urls = []
for instance in session.query(Links).order_by(Links.scrape_date):
    list_of_urls.append(instance.url)

vulnerabilities_list = []
scanner = Scanner(vulnerabilities_list)

def scan(index):
    print('\033[92m Scanning: ' + list_of_urls[index] + ' \033[0m')
    scanner.start_scanning(list_of_urls[index])

# Scan the URLs using 10 threads
print('\033[94m ################################## \033[0m')
print('\033[94m ### Starting scan for ' + str(len(list_of_urls)) + ' urls ###\033[0m')
print('\033[94m ################################## \033[0m')

result = pool.map(scan, range(len(list_of_urls)))

print('\033[94m ################################## \033[0m')
print('\033[94m ### ' + str(len(vulnerabilities_list)) + ' vulnerabilities found. ###\033[0m')
print('\033[94m ################################## \033[0m')

print('Storing recorded vulnerabilities into database...')
for vuln in vulnerabilities_list:
    # Checks if record already exists.
    ret = session.query(exists().where(and_(Vulnerabilities.url == vuln.url, Vulnerabilities.vulnerability_type == vuln.vulnerability_type)))
    record_exist = ret.all()[0][0]
    if record_exist:
        continue

    session.add(vuln)

# Finally commit all vulnerabilities to the DB.
session.commit()
print('Scanning phase complete.\n')

# scanner.start_scanning('https://app5.com/www/index.php')