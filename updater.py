#!/usr/bin/env python

import requests, boto3, logging
from boto3.session import Session

logging.basicConfig(filename='dnsupdater.log',level=logging.INFO)

"""
Add your information to the following variables
$zoneName, $zoneId, $aws_access_key_id,
$aws_secret_access_key
"""
zoneName = ""
zoneId = ""

def sessionDetails():
	"""
	Contains the IAM details to use for initating
	a connection through the boto api
	"""
	session = Session(
        	aws_access_key_id='',
        	aws_secret_access_key='',
        	region_name="eu-west-1",
    	)
	if session:
        	return session

def getPublicIp():
	"""
	Gets the clients public IP address from a number
	of external services, it then checks the results
	against each other for validity.
	"""
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

def modify_record(client, zoneName, zoneId, externalIp, ttl=600):
	"""
	Modifies the zone with the given
	infromation pased through.
	"""
	print client.change_resource_record_sets(
        	HostedZoneId=zoneId,
        	ChangeBatch={
            		'Comment': 'Modified By Dynamic DNS Updater',
            		'Changes': [
                		{
                    		'Action': 'UPSERT',
                    		'ResourceRecordSet': {
                        		'TTL': ttl,
                        		'Name': zoneName,
                        		'Type': 'A',
                        		'ResourceRecords': [
                            		{
                                	'Value': externalIp
                            		},
                        		]
                    		}
                		},
            		]
        	}
    	)

if __name__ == '__main__':
	"""
	Set up the connection to Route53 through
	boto, get the external IP address of the 
	server and then initate a change.
	"""
	session = sessionDetails()
	client = session.client('route53')
	externalIp = getPublicIp()

	logging.info("Updating Zone for {} with IP {}" .format(zoneName, externalIp))
	modify_record(client, zoneName, zoneId, externalIp)
