import boto3
from botocore.client import Config

s3 = boto3.client('s3',
                    endpoint_url='http://192.168.30.100:9000',
                    aws_access_key_id='Go8BtEuqhYghz6uP',
                    aws_secret_access_key='wVMJvmyi9OgXVwWp6RcPnBPeMiOxsdMu',
                    aws_session_token=None,
                    region_name="us-east-1",
                    )

content = "1  Herfelingen 27-12-18\n"\
          "2    Lambusart 14-06-18\n"\
          "3 Spormaggiore 15-04-18"

s3.put_object(Body=content, Bucket="Test", Key="fwf/file1.txt")