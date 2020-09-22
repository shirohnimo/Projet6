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

Stage 1 : 	by now, the playbook will add a rule to allow access on the specified port as a client
			the only option available will additionnally, before adding the rule :
				- add a rule to allow access from SSH on the server
				- set DROP as default to the chains INPUT, OUTPUT and FORWARD
				- flush all the chains
	
	ansible-playbook -i inventory_file --become --ask-become-pass -e "<options> port=number"
		
		options :	init=True	used to clear the table