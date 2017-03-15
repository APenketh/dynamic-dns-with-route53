# Setting Up Dynamic DNS With Amazon Route 53

The concept for this script is to use Amazon's Route 53 DNS to update a domain to point to your home's dynamic IP address. This will enable you to access your home network from outside without the use of any additional software (Which is normally paid for or limited on free accounts). This is perfect for things such as hosting a website or services from your homelab.

Process To Setup This Script:

## Step 1 - Setting Up The AMI User:

To use the AWS API, we’ll need an IAM user profile with relevant permissions.
Log in to the AWS management console and go to Services – IAM – Users and click Create New Users. 

Name the user and give it Programmatic access

![image1](https://cloud.githubusercontent.com/assets/18573773/23434006/a72631d2-fdfc-11e6-8a4c-dc629b103242.PNG)

Click on the "Add user to group", once the next screen has loaded click on "Create Policy" this will open a new screen where you can select "Create Your Own Policy"

Enter the following information:

Policy Name: Something Unique
Description: I suggest putting the github URL for the project here incase you need to reference it in the future

```
{
	"Version": "2012-10-17",
		"Statement": [
			{
				"Sid": "Stmt1488140257000",
				"Effect": "Allow",
				"Action": [
						"route53:ChangeResourceRecordSets"		
				],
						"Resource": [
						"*"
						]	
			}
		]
}
```

So seen here:

![image2](https://cloud.githubusercontent.com/assets/18573773/23434748/1ff20d06-fdfe-11e6-9f6a-dc513908598a.PNG)

Go back on the previous screen, refresh the list and then click on the policy you created, enter a group name and then select create group. Scroll to the bottom of the screen and press "Next: Review" and then "Create user"

You’ll be given an access and secret key. These are used to authenticate the API calls our script will be making. Keep these noted for later in stage 3.

## Step 2: Set up your Route 53 Subdomain

In Route 53 I am going to assume that you already have a domain set up previously, the aim of this step is to set up a subdomain that is going to be altered by the script to point to your home ip whatever it is. For the sake of these instructions I am going to call the subdomain home.

To do this navigate from the AWS Management Console to Services – Route 53 – Hosted Zones. Take note of the Hosted Zone ID of this domain then pick the domain you want to use. 
Click Create Record Set and add the following details:
Name: home
Type: A – IPv4 address (Or AAAA if using IPv6)
TTL (Seconds): 300
Value: 127.0.0.1

Note: Don’t worry that 127.0.0.1 isn’t your your IP address as the script will update this when we first run it.
 
## Step 3: Install the Dynamic DNS Script

First you will need to install the boto3 and requests pip modules for python, if you have pip installed already then you can run the following two commands to install these;

pip install boto3

pip install requests

If you do not already have pip then follow these instructions to install it and then run the commands above: https://pip.pypa.io/en/stable/installing/

Next you can copy the file 'updater.py' from the main repository onto your server or computer or you can clone the repository. Once you have the file on the server you want to change the permissions to allow the execution of the file by the user you want to run the script as. See an example of the command you want to run below;

```
# Add New User To Run The Script As (Best for security)
adduser dynamicdns

# Clone the repository
git clone https://github.com/APenketh/dynamic-dns-with-route53.git

# Changing permissions
chown -R dynamicdns:dynamicdns dynamic-dns-with-route53/
chmod +x dynamic-dns-with-route53/updater.py

# Next you want to edit the crontab for the user you are going to run the script as
su - dynamicdns
crontab -e
     # Add the following line changing the path to your cloned repository (This will run the script every 30 mintuies)
		 */30 * * * * /usr/bin/python /pathtofile/dynamic-dns-with-route53/updater.py
```

Once the script is running your IP address will change to your external IP address within the AWS console, you can check this at any time by logging in and checking the subdomin within route 53.

If you have any issues please feel free to raise an issue here: https://github.com/APenketh/dynamic-dns-with-route53/issues/new
