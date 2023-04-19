import json

with open('../terraform/terraform.tfstate', 'r') as f:
    state = json.load(f)


public_ip = None
private_ips = []

# Get the public ip from the public nodes
public_instance = next((r for r in state['resources'] if r['name'] == 'public_instance'), None)
pub_node_pub_ip = public_instance['instances'][0]['attributes']['public_ip']


# Get the private ip's from the private nodes
private_instances = [r for r in state['resources'] if r['name'] == 'private_instance']
pri_node_pri_address = [i['attributes']['private_ip'] for r in private_instances for i in r['instances']]
# pri_node_pub_address = [i['attributes']['private_ip'] for r in private_instances for i in r['instances']]

# set up the ansible inventory file
with open('../ansible/inventory/inventory.ini', 'w') as f:
    f.write('[public_node]\n')
    f.write("node0 ansible_host={} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws-cluster-key\n".format(pub_node_pub_ip))
    f.write('\n\n[pri_nodes]\n')
    for i in range(0,len(pri_node_pri_address)):
        f.write("node{} ansible_host={} ansible_user=ubuntu ansible_connection=ssh ansible_ssh_private_key_file=../keys/aws-private-cluster-key\n".format(i+1, pri_node_pri_address[i]))
f.close()

# set up the ansible config
with open('../ansible/ansible.cfg', 'w') as f:
    f.write('[defaults]\n')
    f.write('host_key_checking = False\n')
    f.write('inventory = inventory/inventory.ini\n\n')
    f.write('[ssh_connection]\n')
    f.write('ssh_args = -o ProxyCommand="ssh -W %h:%p ubuntu@{}  -i ~/.ssh/aws-cluster-key"'.format(pub_node_pub_ip))
f.close()