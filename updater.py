#!/usr/bin/env python

import requests

def getIp():
	ipDnsomatic = requests.get('http://myip.dnsomatic.com')
	ipCanihazip = requests.get('http://canihazip.com/s')

	if ipDnsomatic.status_code == int(200):
		externalIp = ipDnsomatic.text
	elif ipCanihazip.status_code == int(200):
		externalIp = ipCanihazip.text
	else:
		print("Error: No External Resources Avalible")
	return externalIp

externalIp = getIp()

