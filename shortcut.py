#Due Date: 11/01/2024

#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

#finding all og the symbolic links in the specified directory
def find(directory, link_name=None):
	try: 
		if link_name: #searching for a symbolic link by name
			result = subprocess.run(["find", directory, "type", "l", "-name", link_name], capture_output=True, text=True)
		else: #searching for all symbolic links in a directory
			result = subprocess.run(["find", directory, "-type", "l"], capture_output=True, text=True)
		
		linkies = result.stdout.strip().split("\n") if result.stdout else []
		return linkies
		
	except Exception as exc:
		print(f"Error finding symbolic links: {exc}")
		return []

#Getting the target path of a symbolic link
def read_link(path):
	try:
		return os.readlink(path)
	except Exception as exc:
		print(f"Error finding symbolic links: {exc}.")

#Creating a symbolic link
def ln(link_path, link_name):
	try:
		if not os.path.exists(link_path): #if the path that the user is trying to put the link in does not exist
			print(f"Link path {link_path} does not exist.")
			
		elif os.path.exists(link_name): #if there is already a link with the same name
			print(f"Link {link_name} already exists.")
		else: #if the other two conditions are not met, create a new link using the bash command
			subprocess.run(["ln", "-s", link_path, link_name])
			print(f"Created symbolic link {link_name} and {path}.")
	except Exception as exc:
		print(f"Error creating symbolic link: {exc}.")
		

#Removing a symbolic link
def delete(link_name):
	try: 
		if os.path.islink(link_name): #if the link that the user wants to delete exists
			os.remove(link_name)
			print(f"Removed symbolic link: {link_name}.")
		else: #if the link does not exist
			print(f"{link_name} is not a symbolic link or does not exist.")
			
	except Exception as exc:
		print(f"Error removing symbolic link: {exc}.")

#command to generate a report summarizing the symbolic links on the user's desktop
def generate_report():
	desktop_path = Path.home() / "Desktop" #the home directory
	report_file = desktop_path / "symlink_report.txt" #filename

	linkies = find(str(desktop_path))

	if not linkies: #if there are not any symbolic links
		print("There are no symbolic links on the desktop.")
		return

	#if there are
	try:
		with open(report_file, 'w') as file: #opening the file with the permissions of write
			file.write("=== Symbolic Link Report ===\n")
			file.write(f"Location: {desktop_path}")

			#adding the links found to the report
			for link in linkies:
				target = readLink(link)
				file.write(f"{symlink} -> {target}\n")

			print(f"Report generated: {report_file}") #for user output

			#opening up the file
			open_file(report_file)

	except Exception as e:
		print(f"Error generating report:{e}")

#user experience silliness
def clear_terminal():
	os.system('cls' if os.name == "nt" else 'clear')

def display_menu():
	#user choices
	while True:
		clear_terminal()
		print("=== Available Symbolic Link Commands ===") #header

		#find commands
		print("\t - find <directory>: Lists all of the symbolic links in the specfied directory.")
		print("\t - find <directory> <link_name>: Find a specific symbolic link.")


		#readLine commands -- IDs the target paths
		print("\t - read_link <path>: Identifies the target path of the specified symbolic link.")

		#create links command
		print("\t - ln <path> <link_name>: Creates a symbolic link at the specified path.")

		#remove link command
		print("\t - delete <link_name>: Removes the desired symbolic link.")

		#Generate report command
		print("\t - generate_report: Generates a report of all the symbolic links on the desktop.")

		#Quit command
		print("\t - quit: Exit the program.")

		command = input("\n>").strip().split()

		if not command:
			continue #run it back now y'all

		#time for all the action stuff
		action = command[0].lower()

		#find command
		if action == 'find':
			if len(command) == 2: #just looking in a directory
				directory = command[1]
				linkies = find(directory)
				if linkies: #if there are links
					print("\nFound symbolic links:")
					for link in linkies:
						target = read_link(link)
						print(f"{link} -> {target}.")
				else: #if there are no links to be found
					print("\nNo symbolic links found.")

			elif len(command) == 3: #looking for a specific link
				directory, link_name = command[1], command[2]
				linkies = find(directory, link_name)
				if linkies: #if there are link(s) to be found
					print("\nFoud symbolic link(s):")
					for link in linkies: 
						target = readline(link)
						print(f"{link} -> {target}")
				else: #if there are no links to be found
					print("\nNo matching symbolic links found.")
			else: #invalid syntax
				print("Invalid syntax for 'find'. Use find <directory> or find <directory> <link_name>.")
		input("\nPress Enter to return to the menu.")

		#readLine command
		if action == 'read_link':
			if len(command) == 2:
				path = command[1]
				target = read_link(path)
				if target: #if the target is found
					print(f"{path} -> {target}.")
				else: #if the target is not found
					print(f"Could not read the target of {path}.")
			else: #invalid command syntax
				print("Invalid syntax for 'read_link'. Use readLine <path>.")
			input("\nPress Enter to return to the menu.")

		#create (ln) command
		if action == 'ln':
			if len(command) == 3:
				target, link_name = command[1], command[2]
				ln(target, link_name)
			else: #invalid syntax
				print("Invalid syntax for 'create'. Use create <target> <link_name>.")
			input("\nPress Enter to return to the menu.")

		#remove (delete) command
		if action == 'delete':
			if len(command) == 2:
				link_name = command[1]
				delete(link_name)
			else: #invalid syntax
				print("Invalid syntax for 'delete'. Use delete <link_name>.")
			input("\nPress Enter to return to the menu.")

		#generate_report command
		if action == 'generate_report':
			generate_report()
			input("\nPress Enter to return to the menu.")

		#quit command
		if action == 'quit':
			print("Exiting the program...")
			sys.exit(0)
			
		#reprinting the menu
		if action == 'Enter':
			print("=== Available Symbolic Link Commands ===") #header

			#find commands
			print("\t - find <directory>: Lists all of the symbolic links in the specfied directory.")
			print("\t - find <directory> <link_name>: Find a specific symbolic link.")


			#readLine commands -- IDs the target paths
			print("\t - read_link <path>: Identifies the target path of the specified symbolic link.")

			#create links command
			print("\t - ln <path> <link_name>: Creates a symbolic link at the specified path.")

			#remove link command
			print("\t - delete <link_name>: Removes the desired symbolic link.")

			#Generate report command
			print("\t - generate_report: Generates a report of all the symbolic links on the desktop.")

			#Quit command
			print("\t - quit: Exit the program.")

			command = input("\n>").strip().split()

			if not command:
				continue #run it back now y'all

			#time for all the action stuff
			action = command[0].lower()

		if not((action == 'find') or (action == 'read_link') or (action == 'ln') or (action == 'delete') or (action == 'generate_report') or (action == 'quit') or (action == 'Enter')): #action not found
			print("Unknown command. Please try again...")
			input("\nPress Enter to return to the menu.")
def main():
	display_menu()

if __name__ == '__main__':
	main()
