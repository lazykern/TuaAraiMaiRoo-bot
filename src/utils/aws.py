import os
import boto3
from dotenv import load_dotenv
load_dotenv()
AWS_ACCCESSKEY = os.getenv('AWS_ACCCESSKEY')
AWS_SECRETKEY = os.getenv('AWS_SECRETKEY')
AWS_REGION = os.getenv('AWS_REGION')

session = boto3.session(aws_access_key_id=AWS_ACCCESSKEY,
                        aws_secret_access_key=AWS_SECRETKEY,
                        region_name=AWS_REGION)
dynamodb = session.resource('dynamodb')


GuildsTable = dynamodb.Table('guilds')
GuildsData = GuildsTable.scan()['Items']
GuildIDs = [guild['guildID'] for guild in GuildsData]

cpe35_user_table = dynamodb.Table("aws.cpe35_user_table")
cpe35_y1_exam_table = dynamodb.Table("cpe35_y1_exam")
