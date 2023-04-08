import json

# Open the terraform.tfstate file and load its contents as JSON
with open('../terraform/terraform.tfstate', 'r') as f:
    state = json.load(f)

# Get the private ip's from the private nodes
private_instances = [r for r in state['resources'] if r['name'] == 'private_instance']
pri_node_pri_address = [i['attributes']['private_ip'] for r in private_instances for i in r['instances']]

# Get the public ip from the public nodes
public_instance = next((r for r in state['resources'] if r['name'] == 'public_instance'), None)
control_addr = public_instance['instances'][0]['attributes']['public_ip']


# Write the slurm.config for the nodes
with open('../ansible/slurmconfigs/slurm.conf', 'w') as f:
    # Write the ControlAddr value
    f.write("ControlAddr={}\n".format(control_addr))

    f.write("NodeName=node1 NodeAddr={} CPUs=1 RealMemory=1000 Sockets=1 CoresPerSocket=1 ThreadsPerCore=1 State=UNKNOWN\n".format(control_addr))

    # Write the NodeAddr values
    for i in range(0,len(pri_node_pri_address)):
        f.write("NodeName=node{} NodeAddr={} CPUs=1 RealMemory=1000 Sockets=1 CoresPerSocket=1 ThreadsPerCore=1 State=UNKNOWN\n".format(i+2,pri_node_pri_address[i]))
    f.write("\n\n")
    f.write("ControlMachine=controller({})\n".format(control_addr))
    f.write("SlurmctldHost=conrtoller({})\n".format(control_addr))
    f.write("PartitionName=mycluster Nodes=node[02-{}] Default=YES MaxTime=INFINITE State=UP\n".format((len(pri_node_pri_address)+1)))
    f.write("ClusterName=aws-cluster\n")

    f.write("AccountingStorageType=accounting_storage/none\n")
    f.write("AuthType=auth/munge\n")
    f.write("JobAcctGatherType=jobacct_gather/none\n")
    f.write("JobCompType=jobcomp/none\n")
    f.write("ProctrackType=proctrack/linuxproc\n")
    f.write("ReturnToService=2\n")
    f.write("SchedulerType=sched/backfill\n")
    f.write("SelectType=select/cons_res\n")
    f.write("SelectTypeParameters=CR_Core\n")
    f.write("SlurmUser=slurm\n")
    f.write("SlurmctldDebug=info\n")
    f.write("SlurmctldLogFile=/var/log/slurm/slurmctld.log\n")
    f.write("SlurmctldPidFile=/run/slurmctld.pid\n")
    f.write("SlurmdDebug=info\n")
    f.write("SlurmdLogFile=/var/log/slurm/slurmd.log\n")
    f.write("SlurmdPidFile=/run/slurmd.pid\n")
    f.write("SlurmdPort=6818\n")
    f.write("SlurmdSpoolDir=/var/spool/slurm/d\n")
    f.write("StateSaveLocation=/var/spool/slurm/ctld\n")
    f.write("SwitchType=switch/none\n")
    f.write("TaskPlugin=task/none\n")
f.close()

# Write the cgroups.conf for the nodes
with open('../ansible/slurmconfigs/cgroups.conf', 'w') as f:
    f.write('CgroupMountpoint="/sys/fs/cgroup"\n')
    f.write('CgroupAutomount=yes\n')
    f.write('CgroupReleaseAgentDir="/etc/slurm-llnl/cgroup"\n')
    f.write('AllowedDevicesFile="/etc/slurm-llnl/cgroup_allowed_devices_file.conf"\n')
    f.write('ConstrainCores=no\n')
    f.write('TaskAffinity=no\n')
    f.write('ConstrainRAMSpace=yes\n')
    f.write('ConstrainSwapSpace=no\n')
    f.write('ConstrainDevices=no\n')
    f.write('AllowedRamSpace=100\n')
    f.write('AllowedSwapSpace=0\n')
    f.write('MaxRAMPercent=100\n')
    f.write('MaxSwapPercent=100\n')
    f.write('MinRAMSpace=30\n')
f.close()

# Write the cgroup_allowed_devices_file.conf for the nodes
with open('../ansible/slurmconfigs/cgroup_allowed_devices_file.conf', 'w') as f:
    f.write('/dev/null\n')
    f.write('/dev/urandom\n')
    f.write('/dev/zero\n')
    f.write('/dev/sda*\n')
    f.write('/dev/cpu/*/*\n')
    f.write('/dev/pts/*\n')
f.close()