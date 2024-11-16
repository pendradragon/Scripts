#Megan Kerstetter
#Due Date: 11/15/2024

#! /usr/bin/env python3

import re
import os
from datetime import datetime
from geoip import geolite2
#from operator import itemgetter


#path to the log file on the system
PATH = "/home/student/syslog.log"

#Threshold for failt attempts
THRESHOLD_FAILED = 10

def get_country_from_ip(ip_address):
	match = geolite2.lookup(ip_address)
	if (match is not None) and (match.country is not None): #if there was a country found for the IP address
		return match.country

	return "Unknown" #if the IP address is not found

#helper sorting function
def sort_by_count(item):
	return item[1]

def get_flagged_ips(attempts):
	"""
		Filter and sort the IPs with a number of failed login attempts that meet or exceed the threshold
		Return a list of tuples (IP, amount of times failed) tuples in ASENDING ORDER by the number of failed attempts.
	"""

	flagged_ips=[(ip,count) for ip, count in attempts.items() if count >= THRESHOLD_FAILED]

	return sorted(flagged_ips, key=sort_by_count)

def analyze_log_file():
	attempts = {}
	compromised_servers = set()

	#using regex to find failed login attempts and capture the IP
	failed_login_pattern = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)")
	compromised_server_pattern = re.compile(r"\b([A-Za-z0-9.-]+\.[a-z]{2,6})\b")

	#going through the file
	with open(PATH, 'r') as file:
		for line in file:
			#check to see if the line contains a failed login attempt
			login_match = failed_login_pattern.search(line)
			if login_match: #if the login failed
				address = login_match.group(1)
				attempts[address] = int(attempts.get(address, 0)) + 1

				#check for potentially compromised servers
				server_match = compromised_server_pattern.search(line)
				if server_match: #if the server is potentially compromised
					compromised_servers.add(server_match.group(1)) #adding to the set

	#getting the flagged IPs
	flagged_ips = get_flagged_ips(attempts)

	#generating the report
	os.system('clear' if os.system == 'posix' else 'cls') #clearing the terminal

	#date information for the header
	report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(f"==== Security Report - Date: {report_date} ====\n") #header

	#the actual report
	print(" Count | IP Address       | Country") #table header
	print("-" * 50) #just to make it stand out a little bit more bc pazzaz

	#now it's actually time for the data
	for ip, count in flagged_ips:
		country = get_country_from_ip(ip)
		print(f" {count:<5} | {ip:<15} | {country}") #adding to the table

	#now for the server information
	print("\n Potentially Compromised Servers:\n")
	for server in compromised_servers:
		print(f"\t - {server}")

	#what if I gave the report a pretty little footer? She deserves it
	print("=" * 50) #I hope the report feels bonita bc she looks bonita

if __name__ == "__main__":
	analyze_log_file()
