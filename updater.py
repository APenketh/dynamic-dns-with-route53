#!/usr/bin/env python

import requests
import boto3
import logging

def getPublicIp():
	siteList = ( 'http://myip.dnsomatic.com', 'http://canihazip.com/s' )	
	siteIpReturn = ""

	for sites in siteList:
		siteHolder = requests.get(sites)
		if siteHolder.status_code == int(200):
			if siteIpReturn == "":
				siteIpReturn = siteHolder.text 
			elif siteHolder.text == siteIpReturn:
				siteIpReturn = siteHolder.text
			else:
				print("Replace With Logging2")
		else:
			print("Replace With Logging1")
	return siteIpReturn

externalIp = getPublicIp()
print externalIp
