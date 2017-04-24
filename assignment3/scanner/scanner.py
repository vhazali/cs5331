import requests
from Cookie import SimpleCookie
from loginform import fill_login_form
from urlparse import urlparse
import cookielib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from sqlalchemy import and_
from database.models import Vulnerabilities
from database.models import Inputs

class Scanner:
	# Config data
	accounts = [
	('bryce', 'bryce'),
	('scanner1', 'scanner1'),
	('scanner2', 'scanner2'),
	('admin', 'admin'),
	('student', 'student'),
	('admin', 'adminadmin'),
	('test@test.com', 'testtest'),
	('test@test.com', 'test'),
	('test', 'test'),
	('admin', 'AdminAdmin1!'),
	('test', 'TestTest1!'),
	('user@user.com', 'user'),
	('admin@admin.com', 'admin'),
	('student', 'student'),
	('student2', 'student2')
	]

	# Vulnerability enums
	Session_Hijack = 'Session_Hijack'
	Session_Fixation = 'Session_Fixation'
	Mixed_Content = 'Mixed_Content'
	Predictable_Cookie = 'Predictable_Cookie'

	# Possible cookie keys
	cookie_keys = ['PHPSESSID', 'cookie', 'id', 'session', 'uid', 'cid', 'class']

	def __init__(self, list):
		self.__list = list

		# List of origins, to ensure that there won't be multiple vulnerabilities logged
		self.__list_of_origins = []

	def start_scanning(self, url):
		should_stop = self.__check_if_cookie_is_sent_over_http(url, None)

		# Website is already serving cookie over HTTP, no need to scan anymore.
		if should_stop:
			self.__check_if_cookie_does_not_change_after_login(url)
			self.__check_if_cookie_is_predictable(url)
			return

		self.__check_if_website_has_mixed_content(url)

	# Check #1: To see is cookie is sent in plain over HTTP
	# We force a HTTP request to the website even if it is
	# meant to be served over HTTPS.
	def __check_if_cookie_is_sent_over_http(self, url, given_type):
		response = self.__get_cookies_for(url)
		cookies = response[0]
		if given_type == None:
			given_type = response[1]

		if len(cookies) > 0:
			self.__store_vulnerability(url, given_type, '')
			return True	

		return False

	# Check #2: To see if webpage has mixed content or not.
	# If there is, check #1 is performed on the url of the mixed
	# content.
	def __check_if_website_has_mixed_content(self, url):
		mixed_content_identifier = 'src=\"http://'.lower()
		r = requests.get(url, verify=False)

		if r.status_code != 200:
			return

		# Something is fetched over HTTP
		if mixed_content_identifier in r.text:
			index = r.text.index(mixed_content_identifier)
			end_index = r.text.index('\"', index + len(mixed_content_identifier))
			mixed_content_url = 'http://' + r.text[index + len(mixed_content_identifier) : end_index]

			# Check to see if cookie is sent over the HTTP request
			self.__check_if_cookie_is_sent_over_http(mixed_content_url, Scanner.Mixed_Content)

	# Check #3: To see if a cookie is predictable or not.
	# Removes common substrings from cookies obtained consecutively.
	# If the remaining string is a number, we find out the difference
	# with the highest frequency.
	def __check_if_cookie_is_predictable(self, url):
		# Get a dictionary cookies for a given number of times.
		# Key is the cookie name, value is a list of cookie values.
		NUMBER_OF_COOKIES_TO_TEST = 5
		cookies_dict = self.__get_cookies_for_website_repeatedly(NUMBER_OF_COOKIES_TO_TEST, url)

		for cookie_name, cookies in cookies_dict.iteritems():
			cookies = self.__remove_similar_substrings(cookies)

			# Calculate the frequency of the differences between each 
			# consecutive numeric value.
			prev_value = 0
			differences_dict = {}
			for cookie in cookies:
				# If cookie value is not numeric after removing common
				# substring, then we assume cookie cannot be of a
				# arithmetic progression.
				if not cookie.isdigit():
					return

				difference = int(cookie) - prev_value
				prev_value = int(cookie)
				if difference in differences_dict:
					differences_dict[difference] += 1
				else:
					differences_dict[difference] = 1

			# Get the difference that has the highest frequency
			max_freq = 0
			highest_difference = 0
			for difference, frequency in differences_dict.iteritems():
				if frequency > max_freq:
					max_freq = frequenc
					highest_difference = difference
			self.__store_vulnerability(url, Scanner.Predictable_Cookie, cookie_name + str(highest_difference))

	# Check 4: Check to see if cookie does not change after logging in
	# If cookie does not change after logging in, we can perform session fixation.
	def __check_if_cookie_does_not_change_after_login(self, url):
		if not self.__does_url_have_login_page(url):
			return

		if not self.__check_if_cookies_are_different(url):
			return

		if self.__are_cookies_the_same_after_login(url):
			self.__store_vulnerability(url, Scanner.Session_Fixation, '')

	############################
	# Private helper functions #
	############################

	def __store_vulnerability(self, url, vuln_type, value):
		if self.__is_vulnerability_repeated(url, vuln_type):
			return

		print('\033[91m Scanner: Found vulnerability ' + vuln_type + ' in ' + url + '\033[0m')
		vuln = Vulnerabilities(url=url, vulnerability_type=vuln_type, value=value)
		self.__list.append(vuln)

	# Checks if a given domain and vulnerability_type already exist or not.
	def __is_vulnerability_repeated(self, url, vuln_type):
		given_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))
		for vulnerability in self.__list_of_origins:
			stored_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(vulnerability[0]))
			if stored_domain == given_domain and vulnerability[1] == vuln_type:
				return True
		self.__list_of_origins.append((url, vuln_type))
		return False

	def __get_cookies_for(self, url):
		cookies_dict = {}
		type = Scanner.Session_Hijack
		r = requests.get(url, verify=False)

		if r.status_code != 200:
			type = Scanner.Session_Fixation

		if 'set-cookie' in r.headers:
			cookies_dict = self.__retrieve_cookie_values(r.headers['set-cookie'])
		return (cookies_dict, type)

	def __does_url_have_login_page(self, url):
		engine = create_engine('sqlite:///database/scrapedsites.sqlite')
		Session = sessionmaker(bind=engine)
		session = Session()
		ret = session.query(exists().where(and_(Inputs.url == url, Inputs.type_attr == 'password')))
		record_exist = ret.all()[0][0]

		return record_exist

	def __check_if_cookies_are_different(self, url):
		s = requests.Session()
		s.get(url, verify=False)
		cookies = set(s.cookies.get_dict().values())
		s.get(url, verify=False)
		new_cookies = set(s.cookies.get_dict().values())

		intersection = cookies & new_cookies
		return len(intersection) < len(cookies)

	def __are_cookies_the_same_after_login(self, url):
		r = requests.get(url, verify=False)
		# User login form to get input name and POST url
		response = fill_login_form(url, r.text, "user", "pass")

		user_input_box_name = ''
		pass_input_box_name = ''
		post_url = ''
		for input_tuple in  response[0]:
			if input_tuple[1] == 'user':
				user_input_box_name = input_tuple[0]
			if input_tuple[1] == 'pass':
				pass_input_box_name = input_tuple[0]

		post_url = response[1]

		if not user_input_box_name or not pass_input_box_name or not post_url:
			return

		payload = {}
		for res in response[0]:
			if res[1] == 'user':
				payload[res[0]] = Scanner.accounts[0][0]
			elif res[1] == 'pass':
				payload[res[0]] = Scanner.accounts[0][1]
			else:
				payload[res[0]] = res[1]

		account_index = 1
		is_cookie_the_same = False

		# Actual login using requests

		s = requests.Session()
		login_request = s.post(post_url, data=payload, verify=False)

		while not self.__has_logout_link_in_page(login_request.text) and account_index < len(Scanner.accounts):
			for res in response[0]:
				if res[1] == 'user':
					payload[res[0]] = Scanner.accounts[account_index][0]
				elif res[1] == 'pass':
					payload[res[0]] = Scanner.accounts[account_index][1]
				else:
					payload[res[0]] = res[1]
			login_request = s.post(post_url, data=payload, verify=False)
			account_index += 1

		first = s.cookies.get_dict()
		second_request = s.get(url, verify=False)
		second = s.cookies.get_dict()

		for k1,v1 in first.iteritems():
			for k2,v2 in second.iteritems():
				if k1 == k2 and v1 == v2:
					is_cookie_the_same = True

		return is_cookie_the_same

	def __has_logout_link_in_page(self, html):
		return 'logout' in html.lower()

	def __retrieve_cookie_values(self, raw_string):
		cookies = {}
		cookie = SimpleCookie()
		cookie.load(raw_string)

		for key, morsel in cookie.items():
			if any(name.lower() in key.lower() for name in Scanner.cookie_keys):
				cookies[key] = morsel.value
				
		return cookies

	def __remove_similar_substrings(self, cookies):
		if len(cookies) == 0:
			return

		repeated_sequence = self.__long_substr(cookies) 
		filtered_cookies = []
		for cookie in cookies:
			filtered_cookies.append(cookie.replace(repeated_sequence, ''))

		return filtered_cookies

	# Taken from: http://stackoverflow.com/questions/2892931/longest-common-substring-from-more-than-two-strings-python
	def __long_substr(self, data):
		substr = ''
		if len(data) > 1 and len(data[0]) > 0:
			for i in range(len(data[0])):
				for j in range(len(data[0])-i+1):
					if j > len(substr) and all(data[0][i:i+j] in x for x in data):
						substr = data[0][i:i+j]
		return substr

	def __get_cookies_for_website_repeatedly(self, number_of_times, url):
		cookies_dict = {}
		for i in range(number_of_times):
			for key, value in self.__get_cookies_for(url)[0].iteritems():
				if key in cookies_dict:
					cookies_dict[key].append(value)
				else:
					cookies_dict[key] = [value]
		return cookies_dict

