#!/usr/bin/evn python
from scapy.all import *
def print_summary(pkt):
	if IP in pkt:
		ip_src=pkt[IP].src
		ip_dst=pkt[IP].dst
	if TCP in pkt:
		tcp_sport=pkt[TCP].sport
		tcp_dport=pkt[TCP].dport

		print " IP src " + str(ip_src) + " TCP sport " + str(tcp_sport) 
		print " IP dst " + str(ip_dst) + " TCP dport " + str(tcp_dport)

	# you can filter with something like that
	if ( ( pkt[IP].src == "192.168.0.1") or ( pkt[IP].dst == "192.168.0.1") ):
		print("!")

def http_header(packet):
		http_packet=str(packet)
		if http_packet.find('GET'):
				return GET_print(packet)

def GET_print(packet1):
	ret = "***************************************PACKET****************************************************\n"
	ret += "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
	ret += "*****************************************************************************************************\n"
	return ret

#sniff(filter="ip and host app1.com",prn=print_summary)
sniff(filter="ip and host app1.com",prn=GET_print)

'''
To run scapy, do 
> sudo scapy 

To try sniffing only app1.com 
> pkt = sniff(filter="ip and host app1.com", count=10)

TODO: Trying to get cookie value from packet. but its all encoded :( 
> pkt[9].show()
> pk = pkt[9]
> pktstr = str(pk)
> pktstr.encode('hex')
'''