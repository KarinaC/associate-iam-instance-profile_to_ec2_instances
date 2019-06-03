import boto3  
from botocore.exceptions import ClientError

ec2client = boto3.client('ec2')

def get_list_windows_instances_ids():
	windows_instances_ids = []
	"""gert windows ec2-instances IDs"""
	responses1 = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'platform',
            'Values': [
                'windows',
            ]
        },
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
                'stopped',
            ]
        },
    ],
    DryRun=False,
	)
	for reservations in responses1['Reservations']:
		for instance1 in reservations['Instances']:
			windows_instances_ids.append(instance1["InstanceId"])
	return(windows_instances_ids)



def associate_iam_instance_profile():
	for instance_ids_num in get_list_windows_instances_ids():
		try:
			response = ec2client.associate_iam_instance_profile(
			    IamInstanceProfile={
			        'Arn': 'arn:aws:iam::489768109466:instance-profile/HighroadsEC2andLambdaProfile',
			        'Name': 'HighroadsEC2andLambdaRole'
			    },
			    InstanceId=instance_ids_num
			)
		except ClientError as errork:
			print(errork)
		else:
			print(instance_ids_num +" se agrego iam role")


associate_iam_instance_profile()