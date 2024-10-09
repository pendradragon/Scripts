# Due Date: 10/4/2024

#! /usr/bin/env python3

import os
import platform
import socket
import subprocess

#clears the terminal
def clear_terminal():
	#clears the terminal for different platforms -- ik the instructions said that it only needs to run on linux, but case management
	if os.system == "nt": #Windows OS
		os.system('cls')
	else: #for Mac and Linux OS
		os.system('clear')

#information needed for the "Device Information part of the report -- used for the Device information
def get_domain_name():
	try:
		domain_name = socket.getfqdn().split('.', 1)[1]
	except IndexError:
		domain_name = "No domain found."

	return domain_name

#gets the network info -- each requirement is saved as a key value pair in a dictionary
def get_net_info():
	net_info = {}

	#gets the network interface(s) and addresses
	hostname = socket.gethostname()
	ip_address = socket.gethostbyname(hostname)
	net_info["IP Address"] = ip_address
	
	#Getting the default gateway
	if os.name != "nt": #Mac/Linux
		try:
			route_result = subprocess.run(['ip', 'route'], capture_outpute = True, text = True)
			route_output = route_result.stdout.splitlines()
			for line in route_output:
				if 'default via' in line:
					net_info["Default Gateway"] = line.split()[2]
					break
			
			if_config_result = subprocess.run(['ifconfig'], capture_output = True, text = True)
			ifconfig_output = ifconfig_result.stdout.splitlines()
			
			for line in ifconfig_output:
				if 'inet' in line and 'netmask' in line:
					parts = line.split()
					net_info['Netmask'] = parts[3]
		except Exception as e:
			net_info["Default Gateway"] = "Could not find default gateway"
			net_info["Netmask"] = "Could not find netmask"
	else: #for Windows 
		try:
			ipconfig_result = subprocess.run(['ipconfig'], capture_output = True, text = True)
			ipconfig_result - ipconfig_result.stdout.splitlines()
			
			for line in ipconfig_output:
				if 'IPv4 Address' in line:
					net_info["IP Address"] = line.split(': ')[1]
				elif 'Subnet Mask' in line:
					net_info['Netmask'] = line.split(': ')[1]
				elif 'Default Gateway' in line:
					net_info["Default Gateway"] = line.split(': ')[1]
		except Exception as e:
			net_info['Netmask'] = "Could not find Netmask"
			net_info['Default Gateway'] = "Could not find Default Gateway."
			
	#Gets the DNS info
	if os.name != 'nt':
		try:
			with open('/etc/resolv.conf', 'r') as file:
				dns_servers = [line.split()[1] for line in file if line.startswith('nameserver')]
				net_info["DNS 1"] = dns_servers[0] if len(dns_servers) > 0 else "DNS 1 not found"
				net_info["DNS 2"] = dns_servers[1] if len(dns_servers) > 1 else "DNS 2 not found"
				
		except FileNotFoundError:
			net_info["DNS 1"] = "DNS 1 not found"
			net_info["DNS 2"] = "DNS 2 not found"

	return net_info
	
def get_processor_info():
	processor_info = {}
	
	if os.name != 'nt':
		try:
			lscpu_result = subprocess.run(['lscpu'], capture_output = True, text = True)
			lscpu_output = lscpu_result.stdout.splitlines()
			for line in lscpu_output:
				if 'Model name' in line:
					processor_info["CPU Model"] = line.split(':')[1].strip()
				elif 'Socket(s)' in line:
					processor_info["Number of Processors"] = line.split(':')[1].strip()
				elif 'Core(s) per socket' in line:
					processor_info["Number of Cores"] = line.split(':')[1].strip()
		
		except Exception as e:
			processor_info["Error"] = str(e)

	return processor_info

#gets the information needed for the log, stored in an array
def get_report_stats():
	#local variable used to store report information
	report = []

	#Device information section
	report.append("~~~ Device information ~~~") #header

	hostname = socket.gethostname()
	domain_name = get_domain_name()

	report.append(f"Hostname:\t{hostname}")
	report.append(f"Domain:\t{domain_name}")

	#Network information section
	report.append("\n~~~ Network information ~~~") #header

	network_info = get_net_info()
	for key, value in network_info.items():
		report.append(f"{key}:\t{value}")

	#The OS information
	report.append("\n~~~ OS Information ~~~") #header

	os_info = platform.system()
	os_version = platform.version()
	kernel_version = platform.release()

	report.append(f"Operating System:\t{os_info}")
	report.append(f"Operating Version:\t{os_version}")
	report.append(f"Kernel Version:\t{kernel_version}")

	#Storage Information
	report.append("\n~~~ Storage Information ~~~")

	if os.name != 'nt':
		disk_info = os.statvfs('/')
		total_space = disk_info.f_frsize * disk_info.f_blocks / (1024 * 1024 * 1024)
		available_space = disk_info.f_frsize * disk_info.f_bavail / (1024 * 1024 * 1024)
		
		report.append(f"Hard Drive Capacity:\t{total_space:.2f} GB")
		report.append(f"Available Space:\t{available_space:.2f} GB")


	#Processor Information
	report.append ("\n~~~ Processor Information ~~~")
	processor_info = get_processor_info() #helper function goes brrr

	for key, value in processor_info:
		report.append(f"{key}:\t{value}")

	#Memory Information
	report.append("\n~~~ Memory Information ~~~")
	
	if os.name != 'nt':
		try:
			free_result = subprocess.run(['free', '-h'], capture_output = True, text = True)
			free_output = free_result.stdout.splitlines()
			memory_info = free_output[1].split()
			
			#adding things to the report
			report.append(f"Total RAM:\t{memory_info[1]}")
			report.append(f"Available RAM:\t{memory_info[6]}")
		
		except Exception as e:
			report.append(f"Memory Information Error:\t{str(e)}")

	#returns the report so it can be read and iterated through by the log later
	return report

#makes the log file
def write_log(report):
	#saves the log to the user's home directory
	home_directory = os.path.expanduser("~")

	#gets the hostname
	hostname = socket.gethostname()

	#makes the log file
	log = os.path.join(home_directory, f"{hostname}_system_report.log")

	#writes the report created above to the log file
	with open(log, 'w') as file:
		file.write(report)

#main function
if __name__ == "__main__":
	clear_terminal()

	report = get_report_stats()

	#prints the report
	for item in report:
		print(item)

	#saves the report to the log
	write_log(report)
