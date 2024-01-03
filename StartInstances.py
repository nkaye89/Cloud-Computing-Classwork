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
        
def main():
    num = 1     #change to amount of instances you want created
    start_instances(num)
    

main()