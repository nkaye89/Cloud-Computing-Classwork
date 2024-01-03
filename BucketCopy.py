import botocore
import boto3

#Creating Session With Boto3.
session = boto3.Session(
aws_access_key_id='______',             # insert acess key id
aws_secret_access_key='______'          # insert secret access key
)

#Creating S3 Resource From the Session.
s3 = session.resource('s3')

srcbucket = s3.Bucket('mu2022class')    # replace with source bucket name
srcExists = True
try:
    s3.meta.client.head_bucket(Bucket='mu2022class')    # replace with source bucket name
except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

destbucket = s3.Bucket('nkayebucket')                   # replace with destination bucket name
destExists = True
try:
    s3.meta.client.head_bucket(Bucket='nkayebucket')    # replace with destination bucket name
except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

# Iterate All Objects in Your S3 Bucket Over the for Loop
for obj in srcbucket.objects.all():
    
    #Create a Soucre Dictionary That Specifies Bucket Name and Key Name of the Object to Be Copied
    copy_source = {
    'Bucket': 'mu2022class',                            # replace with source bucket name
    'Key': obj.key
    }
    print(obj.get()['Body'].read().decode('utf-8'))
    destbucket.copy(copy_source, obj.key)