# Creating a High Performance Computing Cluster with Terraform and Ansible
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Terraform_Logo.svg/1920px-Terraform_Logo.svg.png" width="100"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://upload.wikimedia.org/wikipedia/commons/2/24/Ansible_logo.svg" width="100"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" width="100"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1920px-Amazon_Web_Services_Logo.svg.png" width="100"/>
## Project Description

The objective of this project was to create and administer an HPC cluster on [AWS](https://aws.amazon.com/), running [Slurm](https://slurm.schedmd.com/overview.html) with [Terraform](https://www.terraform.io/) and [Ansible](https://www.ansible.com/). 

This was a final research project for my High Performance Computing class at [Trent University](https://www.trentu.ca/)


## What Does This Project Do?

1. Creates AWS infrastructure as defined in the `terraform/cluster.tf` file. This is
   - one login node
   - however many compute nodes as defined in the `terraform/terraform.tfvars` file. 
   - The network rules are set so that to ssh into any of the compute nodes, you must proxy through the login node. This is to reduce the cyber attack surface to just one machine rather than the entire cluster.
2. Runs python scripts to generate:
   - The Ansible inventory and config file,
   - The `slurm.config` file for slurm,
   - the `/etc/hosts` for the machines so they can communicate through slurm easily.
3. Runs Ansible playbooks against each nodes, setting up:
   - Updates each machine,
   - Sets permissions on directories needed for slurm,
   - Munge (required for slurm),
   - the slurmd and slurmctld.
## Steps to Run:
1. You should be running this on a Linux machine (this could work on Mac or Windows, but I have no experience with them).
2. You need aws account with ec2 permissions
   1. You specifically need the access key and secret access key from this account.
3. Install the following software:
   1. [terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
   2. [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
   3. [python](https://www.python.org/downloads/)
4. Create ssh keys on your machine with `ssh keygen`
   1. ~/.ssh/aws-cluster-key.pub
   2. keys/nodekey.pub
   3. keys/aws-private-cluster-key.pub
5. export the aws credentials as env variables
   1. export AWS_ACCESS_KEY_ID="anaccesskey"
   2. export AWS_SECRET_ACCESS_KEY="asecretkey"
6. initialize terraform
   1. terraform init
7. Modify the `terraform/terraform.tfvars` file to set the amount of compute nodes you need, and the [size of the AWS instance](https://aws.amazon.com/ec2/instance-types/) you need. 
   - Note: this doesn't work with any of the free tier options. Slurm has trouble running with the network speed the t2.micro. t3.small is the default and works.
8. run the ./create_cluster.sh script and answer 'yes' to the prompts from terraform, and adding the key to known_hosts.
9. Take note of the public ip printed by terraform, or get it later from the Ansible inventory to ssh into the login node.
10. Once Ansible is finished, ssh into the login node with `ssh ubuntu@the-login-node-ip`. Run `sinfo` to see your compute cluster, and [run some slurm commands](https://hpc.nmsu.edu/discovery/slurm/slurm-commands/) to shcedule your jobs.


## License
This project is licensed under the terms of the GNU GENERAL PUBLIC LICENSE.
