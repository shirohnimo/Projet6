#!/home/user-ansible/ansible2.9.13/bin/python3

import sys
import argparse
import ansible_runner

# Arguments used in command line :
parser = argparse.ArgumentParser()
parser.add_argument("port", type=int, help="Port number to open in netfilter")
parser.add_argument("-s", "--server", action="store_true", help="Specifies to open the port in server mode")
parser.add_argument("-i", "--init", action="store_true", help="Clear netfilter tables")
args = parser.parse_args()

# Set variable 'mode', by default to 'client'
if args.server:
	mode='server'
else:
	mode='client'

# Launch the Ansible playbook
r = ansible_runner.run(
	private_data_dir='/home/user-ansible/Projet6',
	playbook='AddRule.yml',
	inventory='inventaire.ini',
	extravars={'init': args.init, 'port': args.port, 'mode': mode},
	cmdline='-b -K',
	passwords={"BECOME password: ": "passforce"},
	quiet=True
	)

# Display results
print("{}: {}".format(r.status, r.rc))
print("Final status:")
print(r.stats)