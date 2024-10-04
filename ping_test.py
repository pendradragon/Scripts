# 9/17/24

#it's shebang time B)

#!/usr/bin/env python3

import os
import subprocess
import socket

#clears the terminal so there is space for the menu
def clearTerminal():
	#for Windows machines
	if os.name ==  'nt':
		os.system('cls')

	#for all other os-s
	else:
		os.system('clear')

def displayMenu():
	print("==========Menu==========")
	print("1." + "\t" + "Display the defualt gateway")
	print("2." + "\t" + "Test Local Connectivity")
	print("3." + "\t" + "Test Remote Connectivity")
	print("4." + "\t" + "Test DNS Resolution")
	print("5." + "\t" + "Quit")
	print("========================")

#gets the defualt gateway from running "ipconfig" -- this function should run with OPTION 1
def getDefaultGateway() :
	print("Running default gateway...")
	try:
		# for Windows OS-s
		if os.name == "nt":
			#runs ipconfig and records the result so it can be looked through
			result = subprocess.run(["ipconfig"], capture_output = True, text=True) #should save results as text -- look throught each line like a file
			for line in result.stdout.splitlines():
				# if "default gateway" is in the results
				if "Default Gateway" in line:
					gateway = line.split(":")[-1].strip()
					if gateway:
						print(gateway)


		# for other Os-s
		else:
			#runs the ipconfig for linux
			result = subprocess.run(["ip", "route"], capture_output = True, text = True)
			for line in result.stdout.splitlines():
				if "default via" in line:
					print(line.split()[2])
	except Exception as catcher:
		print (f"Error: {catcher}")


	#if there is no default gateway
	print ("There was no default gateway found.")

#tests the local connection via pings -- should be paired to OPTION 2
def testLocalConnectivity():
	try:
		#for Windows OS
		if os.name == "nt":
			result = subprocess.run(["ping", "127.0.0.1"], capture_output = True, text = True)
		#for the other OS-s
		else:
			result = subprocess.run(["ping", "-c", "4", "127.0.0.1"], capture_output = True, text = True)


		#parsing the information that was given by the ping command
		if "Reply from" in result.stdout or "64 bytes from" in result.stdout:
			print( "Local Connectivity Test Passed.")
		else:
			print("Local Connectivity Test Failed")

	except Exception as catcher:
		print (f"Error: {catcher}")

# checking the remote host -- should be tied to OPTION 3
def checkRemoteHost():
	# should ping  129.21.3.17
	try:
		# for Windows OS
		if os.name == "nt":
			result = subprocess.run(["ping", "129.21.3.17"], capture_output = True, text = True)
		#for other OS-s
		else:
			result = subprocess.run(["ping", "-c" , "4", "129.21.3.17"], capture_output = True, text = True)

		#parsing the results from the ping
		if "Reply from" in result.stdout  or "64 bytes from" in result.stdout:
			print( "Successfully connected to 129.21.3.17")
		else:
			print(  "Failed to connect to 129.21.3.17")

	except Exception as catcher:
		return (f"Error: {catcher}")

# testing the DNS resolution -- should be tied to OPTION 4
def testDNSResolution():
	try:
		ipAddress = socket.gethostbyname("www.google.com")
		print( "DNS Resolution Successful: 'www.google.com' resolved to {ipAddress}")

	except socket.gaierror:
		return (f"DNS Resolution failed for 'www.google.com' ")


# throwing it all together
def main():
	while True:
		#starting the terminal
		clearTerminal()
		displayMenu()

		#user input
		option = input("Select an option: ").strip()
		
		#debugging because this code is mean
		#print(f"The user selected option '{option}' ")

		#using the user input
		if option  == '1':
			getDefaultGateway()
			input("\n" + "Press Enter to continue")
		elif option  == '2':
			testLocalConnectivity()
			input("\n" + "Press Enter to continue")
		elif option  == '3':
			checkRemoteHost()
			input("\n" + "Press Enter to continue")
		elif option == '4':
			testDNSResolution()
			input("\n" + "Press Enter to continue")
		elif option  == '5':
			print("Now exitting...")
			break
		else:
			print("Invalid option.\n")
			displayMenu()
			option = input("Select an option: \t")

if __name__ == "__main__":
	main()
