#!/bin/sh -eux

cd `dirname $0`
cd ../

ansible-playbook -i ansible/inventory_file ansible/playbook.yml -e 'ansible_python_interpreter=/usr/bin/python3'
