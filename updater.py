#!/usr/bin/env python

import requests
import boto3
import logging

logging.basicConfig(filename='dnsupdater.log',level=logging.INFO)

def getPublicIp():
	siteList = ( 'http://myip.dnsomatic.com', 'http://canihazip.com/s' )	
	siteIpReturn = ""

	for sites in siteList:
		siteHolder = requests.get(sites)
		if siteHolder.status_code == int(200):
			if siteIpReturn == "":
				siteIpReturn = siteHolder.text 
				logging.info(" Site: '{0}' provided IP: '{1}'" .format(sites, siteHolder.text))
			elif siteHolder.text == siteIpReturn:
				siteIpReturn = siteHolder.text
				logging.info(" Site: '{0}' provided IP: '{1}'" .format(sites, siteHolder.text))
			else:
				logging.warning(" Site: '{0}' provided IP address '{1}' which did not match the last provided IP address of '{2}', please investigate manually." .format(sites, siteHolder.text, siteIpReturn))
		else:
			logging.warning(" Site: '{0}' is not currently working." .format(sites))
	return siteIpReturn

externalIp = getPublicIp()
