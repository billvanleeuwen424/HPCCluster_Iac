#!/bin/bash

cd terraform
terraform apply

cd ../python
python inventory.py

cd ../ansible
ansible-playbook publicnode.yml
ansible-playbook prinodes.yml
