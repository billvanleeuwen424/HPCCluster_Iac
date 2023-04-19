import json

# Open the terraform.tfstate file and load its contents as JSON
with open('../terraform/terraform.tfstate', 'r') as f:
    state = json.load(f)

# Get the private ip's from the private nodes
private_instances = [r for r in state['resources'] if r['name'] == 'private_instance']
pri_node_pri_address = [i['attributes']['private_ip'] for r in private_instances for i in r['instances']]

# Get the public ip from the public nodes
public_instance = next((r for r in state['resources'] if r['name'] == 'public_instance'), None)
control_addr = public_instance['instances'][0]['attributes']['private_ip']

#make the hostname for slurm
ip_parts = control_addr.split(".")
control_hostname = "ip-" + "-".join(ip_parts)


# Write the slurm.config for the nodes
with open('../ansible/slurmconfigs/slurm.conf', 'w') as f:

    f.write("NodeName=node[1-{}] CPUs=2 Sockets=1 CoresPerSocket=1 ThreadsPerCore=2 State=UNKNOWN\n".format(len(pri_node_pri_address)))

    f.write("\n\n")
    # f.write("ControlMachine=node0\n")
    # f.write("ControlAddr=node0\n")
    f.write("SlurmctldHost=node0\n")
    f.write("PartitionName=mycluster Nodes=ALL Default=YES MaxTime=INFINITE State=UP\n")
    f.write("ClusterName=aws-cluster\n")

    f.write("MpiDefault=none\n")
    f.write("ProctrackType=proctrack/linuxproc\n")
    f.write("ReturnToService=1\n")
    f.write("SlurmctldPidFile=/run/slurmctld.pid\n")
    f.write("SlurmdPort=6818\n")
    f.write("SlurmctldPort=6817\n")
    f.write("SlurmdPidFile=/run/slurmd.pid\n")
    f.write("SlurmdSpoolDir=/var/spool/slurmd.spool\n")
    f.write("SlurmUser=slurm\n")
    f.write("StateSaveLocation=/var/spool/slurm.state\n")
    f.write("SwitchType=switch/none\n")
    f.write("TaskPlugin=task/affinity,task/cgroup\n")
    f.write("InactiveLimit=0\n")
    f.write("KillWait=30\n")
    f.write("MinJobAge=300\n")
    f.write("SlurmctldTimeout=120\n")
    f.write("SlurmdTimeout=300\n")
    f.write("Waittime=0\n")
    f.write("SchedulerType=sched/backfill\n")
    f.write("JobCompType=jobcomp/none\n")
    f.write("JobAcctGatherFrequency=30\n")
    f.write("JobAcctGatherType=jobacct_gather/none\n")
    f.write("SlurmctldDebug=info\n")
    f.write("SlurmctldLogFile=/var/log/slurm/slurmctld.log\n")
    f.write("SlurmdDebug=info\n")
    f.write("AccountingStorageType=accounting_storage/none\n")
    f.write("SlurmdLogFile=/var/log/slurm/slurmd.log\n")

f.close()

# Write the cgroups.conf for the nodes
with open('../ansible/slurmconfigs/cgroups.conf', 'w') as f:
    f.write('CgroupMountpoint=/sys/fs/cgroup\n')
    f.write('CgroupAutomount=yes\n')
    f.write('CgroupReleaseAgentDir=/etc/slurm-llnl/cgroup\n')
    f.write('AllowedDevicesFile=/etc/slurm-llnl/cgroup_allowed_devices_file.conf\n')
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