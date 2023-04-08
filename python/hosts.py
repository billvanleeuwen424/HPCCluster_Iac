import json

with open('../terraform/terraform.tfstate', 'r') as f:
    state = json.load(f)


public_ip = None
private_ips = []

# Get the public ip from the public nodes
public_instance = next((r for r in state['resources'] if r['name'] == 'public_instance'), None)
pub_node_pub_ip = public_instance['instances'][0]['attributes']['public_ip']
pub_node_pri_ip = public_instance['instances'][0]['attributes']['private_ip']


# Get the private ip's from the private nodes
private_instances = [r for r in state['resources'] if r['name'] == 'private_instance']
pri_node_pri_address = [i['attributes']['private_ip'] for r in private_instances for i in r['instances']]
# pri_node_pub_address = [i['attributes']['private_ip'] for r in private_instances for i in r['instances']]

with open('../ansible/hosts/hosts', 'w') as f:

    # the stuff directly below is already in the nodes hosts file by default
    f.write('127.0.0.1 localhost\n')
    f.write('\n# The following lines are desirable for IPv6 capable hosts\n')
    f.write('::1 ip6-localhost ip6-loopback\n')
    f.write('fe00::0 ip6-localnet\n')
    f.write('ff00::0 ip6-mcastprefix\n')
    f.write('ff02::1 ip6-allnodes\n')
    f.write('ff02::2 ip6-allrouters\n')
    f.write('ff02::3 ip6-allhosts\n\n')

    f.write("{}      node1\n".format(pub_node_pri_ip))
    for i in range(0,len(pri_node_pri_address)):
        f.write("{}      node{}\n".format(pri_node_pri_address[i], i+2))
f.close()