import json

# Open the terraform.tfstate file and load its contents as JSON
with open('../terraform/terraform.tfstate', 'r') as f:
    state = json.load(f)

# Extract the public and private IP addresses of each EC2 instance in the state file
public_ip = None
private_ips = []
for resource in state['resources']:
    if resource['type'] == 'aws_instance':
        for instance in resource['instances']:
            private_ip = instance['attributes'].get('private_ip', None)
            public_ip_attr = resource['instances'][0]['attributes'].get('public_ip', None)
            if public_ip_attr:
                public_ip = public_ip_attr
            if resource['name'] == 'private_instance':
                private_ips.append(private_ip)

# Write the public IPs to an Ansible inventory file
with open('../ansible/inventory/inventory.ini', 'w') as f:
    f.write('[public_node]\n')
    f.write("ubuntu0 ansible_host={} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws-cluster-key\n".format(public_ip))
    f.write('\n\n[pri_nodes]\n')
    for i in range(0,len(private_ips)):
        f.write("ubuntu{} ansible_host={} ansible_user=ubuntu ansible_connection=ssh ansible_ssh_private_key_file=../keys/aws-private-cluster-key\n".format(i+1, private_ips[i]))
f.close()

# set up the ansible config
with open('../ansible/ansible.cfg', 'w') as f:
    f.write('[defaults]\n')
    f.write('host_key_checking = False\n')
    f.write('inventory = inventory/inventory.ini\n\n')
    f.write('[ssh_connection]\n')
    f.write('ssh_args = -o ProxyCommand="ssh -W %h:%p ubuntu@{}  -i ~/.ssh/aws-cluster-key"'.format(public_ip))
f.close()