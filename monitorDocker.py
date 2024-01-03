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

def install_docker():
    ec2 = boto3.resource('ec2')
    pkey = paramiko.RSAKey.from_private_key_file("/path/key.pem")   # insert path and .pem file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in ec2.instance.all():
        if(i.state['Name'] == 'running'):
            print('connecting to instance '+ i.id)
            host = i.public_ip_address
            ssh.connect(host, username = "ubuntu", pkey=pkey)
            print("connected to instance "+ i.id)
            stdin, stdout, stderr = ssh.exec_command("sudo apt-get update")
            stdin, stdout, stderr = ssh.exec_command("sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin")
            
    stdin.close()
    stdout.close()
    stderr.close()
    print('docker installed on all running instances')

def monitor_containers():
    ec2 = boto3.resource('ec2')
    pkey = paramiko.RSAKey.from_private_key_file("/path/key.pem")   # insert path and .pem file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        for i in ec2.instances.all():
            if(i.state['Name'] == 'running'):
                print("connecting to instance "+ i.id)
                name = i.public_dns_name
                ssh.connect(hostname = name, username = "ubuntu", pkey=pkey)
                print ("connected to instance"+ i.id)
                stdin, stdout, stderr = ssh.exec_command("docker run -d -t ubuntu sh")
                stdin, stdout, stderr = ssh.exec_command("docker ps | grep ubuntu")
                container_ID = stdout
                stdin, stdout, stderr = ssh.exec_command("docker exec container_ID top -bn1 | grep CPU")
                output = stdout.read()
                print("container "+ container_ID +" in instance "+ i.id +"\tcpu usage: "+ output)
                stdin.close()
                stdout.close()
                stderr.close()
                ssh.close()
                print("exited from instance "+ i.id)
                time.sleep(5)
        
def main():
    num = 1     #change to amount of instances you want created
    start_instances(num)
    monitor_containers()
    

main()