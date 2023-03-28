import json

# Open the terraform.tfstate file and load its contents as JSON
with open('../terraform/terraform.tfstate', 'r') as f:
    state = json.load(f)

# Extract the public IP address of each EC2 instance in the state file
public_ips = []
for resource in state['resources']:
    if resource['type'] == 'aws_instance':
        public_ip = resource['instances'][0]['attributes'].get('public_ip', None)
        if public_ip:
            public_ips.append(public_ip)

# Write the public IPs to an Ansible inventory file
with open('../ansible/inventory/host_node.ini', 'w') as f:
    f.write('[host_node]\n')
    for ip in public_ips:
        f.write("ubuntu1 ansible_host=" + ip + " ansible_user=ubuntu" + " ansible_ssh_private_key_file=~/.ssh/aws-cluster-key" + '\n')
