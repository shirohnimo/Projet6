#!/home/user-ansible/ansible2.9.13/bin/python3

import sys
import argparse
import ansible_runner
import json

# Variables
work_dir = '/home/user-ansible/Projet6'		# Working Directory
data_file = 'env/data.json'					# File containing ports list to filter
pb_file = 'AddRule.yml'						# Name of the playbook file
inv_file = 'inventaire.ini'					# Ansible inventory file
become_pass = 'passforce'					# Become password for Ansible user

# Arguments used in command line :
parser = argparse.ArgumentParser()
parser.add_argument("port", nargs='?', type=int, help="Port number to open in netfilter, content of env/data.json used if omitted")
parser.add_argument("-u", "--udp", action="store_true", help="Specifies to open the port in UDP protocol (by default TCP is used)")
parser.add_argument("-s", "--server", action="store_true", help="Specifies to open the port in server mode")
parser.add_argument("-d", "--destination", type=str, help="Name of the destination server")
parser.add_argument("-i", "--init", action="store_true", help="Clear netfilter tables")
args = parser.parse_args()

# Read the data_file and return rules order and list
def ReadData(file):
	rules_order = []
	rules_list = []

	with open(file) as f:
		data = json.load(f)
	for entry in data:
		for rank, rule in entry.items():
			rules_order.append(rank)
			rules_list.append(rule)
	return(rules_order, rules_list)


# Launch an Ansible playbook to create a netfilter rule
def RunPlaybook(port, protocol, mode, init, target):
	# Setting target to default group 'netfilter' if omitted
	if target is None:
		target = 'netfilter'

	# Display activity
	if init:
		print("Initialisation des tables.\n")
	print("Application de la règle sur le port {} {}, en mode {} sur {}.\n".format(port, protocol, mode, target))
	
	# Launch the Ansible playbook
	r = ansible_runner.run(
		private_data_dir=work_dir,
		playbook=pb_file,
		inventory=inv_file,
		extravars={'init': init, 'port': port, 'protocol': protocol, 'mode': mode, 'target': target},
		cmdline='-b -K',
		passwords={"BECOME password: ": become_pass},
		quiet=True
		)

# Launch the playbook for each port in data_file
def ApplyFromFile():
	data = ReadData(data_file)
	rules_order = data[0]
	rules_list = data[1]
	for i in range(0,len(rules_order)):
		port = int(rules_list[i].split(', ')[0])
		protocol = rules_list[i].split(', ')[1]
		mode = rules_list[i].split(', ')[2]
		RunPlaybook(port, protocol, mode, args.init, args.destination)
		args.init = False

# Launch the playbook with values entered as arguments
def ApplyFromCLI():
	if args.udp:
		protocol = 'udp'
	else:
		protocol = 'tcp'

	if args.server:
		mode = 'server'
	else:
		mode = 'client'

	RunPlaybook(args.port, protocol, mode, args.init, args.destination)

# If port specified as argument, apply for this port
if args.port:
	ApplyFromCLI()
# otherwise, apply for each port in data file
else:
	ApplyFromFile()