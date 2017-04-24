import pyshark
import threading
from trollius.executor import TimeoutError

# Callback for sniffer.start_sniffing
# def sniffing_callback(cookie_detected, cookie):
# 	if cookie_detected:
# 		print("COOKIE FOUND: " + cookie)
# 	else:
# 		print("COOKIE NOT FOUND")

class Sniffer:

	def __init__(self):
		pass

	def start_sniffing(self, callback_function):
		t = threading.Thread(target=self.__sniff, args=(callback_function,))
		t.start()

	def __sniff(self, callback_function):
		capture = pyshark.LiveCapture(interface='eth0', display_filter='http')
		capture.sniff(timeout=8)
		
		# Look through the packets for a cookie value
		for i in range(0, len(capture)):
			packet = capture[i]

			if hasattr(packet['http'], 'cookie'):
	 			callback_function(True, packet['http'].cookie)
	 			return

	 	callback_function(False, None)
