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
            else:
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
    f.write('inventory = inventory/inventory.ini\n\n')
    f.write('[ssh_connection]\n')
    f.write('ssh_args = -o ProxyCommand="ssh -W %h:%p ubuntu@{}  -i ~/.ssh/aws-cluster-key"'.format(public_ip))
f.close()

# set up the squid configuration
with open('../ansible/templates/squid.conf.j2', 'w') as f:
    f.write('acl allowed_ips src ')
    for i in private_ips:
        f.write('{} '.format(i))
    f.write('\nhttp_access allow allowed_ips\n')
    f.write('\nhttp_port 3128\n')
    f.write('cache_dir ufs /var/spool/squid 100 16 256\n')
    f.write('access_log /var/log/squid/access.log squid\n')
    f.write('cache_mem 256 MB\n')
    f.write('maximum_object_size 4 MB\n')
    f.write('visible_hostname squid-proxy\n')