import boto3
import paramiko
import time

def start_instances(num_instances):
    ec2 = boto3.resource('ec2')
    ec2.create_instances(ImageId='ami-id',              # insert ami-id
        InstanceType='t2.micro',
        MaxCount=num_instances,
        MinCount=num_instances,
        KeyName='key',                                  # insert key name
        SecurityGroupIds=['sg-id',])                    # insert sg-id

    for i in ec2.instances.all():
        if(i.state['Name'] == 'pending'):
            i.wait_until_running()
            i.load()
            print(i.id)      
    print('all pending instances started\n')

def monitor_instances():
    ec2 = boto3.resource('ec2')
    pkey = paramiko.RSAKey.from_private_key_file("./key.pem")   # insert .pem file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        for i in ec2.instances.all():
            if(i.state['Name'] == 'running'):
                print("connecting to instance "+ i.id)
                name = i.public_ip_address
                print(name)
                ssh.connect(hostname = name, username = "ubuntu", pkey=pkey)
                print ("connected to instance"+ i.id)
                stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep Cpu")
                output = stdout.read()
                print("instance "+ i.id +"\tcpu usage: "+ output)
                ssh.close()
                print("exited from instance "+ i.id)
                time.sleep(5)
        
def main():
    num = 1     #change to amount of instances you want created
    start_instances(num)
    monitor_instances()
    

main()