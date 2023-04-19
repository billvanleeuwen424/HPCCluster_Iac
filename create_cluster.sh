#!/bin/bash

cd terraform
terraform apply

sleep 5

cd ../python
python inventory.py
python slurm_config.py
python hosts.py

sleep 5

cd ../ansible
ansible-playbook publicnode.yml
ansible-playbook prinodes.yml
