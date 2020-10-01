# Projet6
Ansible module in Python

The aim of the project is to create an Ansible module in python language.
I'm planning to create and maybe implement an iptables file created with data in a JSON file

My sheduled steps are :
1) Create an Ansible playbook to push one iptables rule on a server
2) Code a script in python invoking the basic playbook previously created
3) Update the python script to load the JSON file and apply the playbook for each data
4) Create the Ansible module invoking the python script

Future updates if enough time left
* python script to manage/update the JSON file
* update the script to apply the new content with the Ansible module

Usage :

Stage 1 : 	the playbook will add a rule to allow communication on the specified port as a client
		the playbook will run on all hosts in group "netfilter" if no target defined in options
			
	ansible-playbook -i inventory_file --become --ask-become-pass -e "<options>" AddRule.yml
		
		options :	init=True		used to clear the table and set a rule to allow SSH access
				port=<number>		specified port for the new rule, no rule created if ommited
				protocol=udp		change protocol to UDP (TCP if ommited)
				mode=server		the specified port will be unlocked as a service (mode client if omitted)
				target=<server>		host targetted by the playbook (must be in inventory file)

Stage 2 & 3 :
		the python script uses the AddRule Ansible playbook to create netfiler rules
		the script apply the playbook for every port in a JSON file (env/data.json)

	usage: rule_iptable.py [-h] [-u] [-s] [-d DESTINATION] [-i] [port]

	positional arguments:
  		port                  Port number to open in netfilter, content of env/data.json used if omitted

	optional arguments:
  		-h, --help            				Show this help message and exit
  		-u, --udp          				Specifies to open the port in UDP protocol (by default TCP is used)
  		-s, --server     				Specifies to open the port in server mode
  		-d DESTINATION, --destination DESTINATION	Name of the destination server
  		-i, --init  				        Clear netfilter tables
