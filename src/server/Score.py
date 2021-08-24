import discord
from discord import embeds
from discord_slash import SlashContext
from discord import Embed
import boto3
import os
import discord_slash
from dotenv import load_dotenv


colors = {'fail': 0xb01111,
          'pass': 0x37e407}

load_dotenv()
AWS_ACCCESSKEY = os.getenv('AWS_ACCCESSKEY')
AWS_SECRETKEY = os.getenv('AWS_SECRETKEY')
AWS_REGION = os.getenv('AWS_REGION')
session = boto3.Session(aws_access_key_id=AWS_ACCCESSKEY,
                        aws_secret_access_key=AWS_SECRETKEY,
                        region_name=AWS_REGION)
dynamodb = session.resource("dynamodb")

cpe35_server_user = dynamodb.Table("cpe35_server_user")
cpe35_y1_exam = dynamodb.Table("cpe35_y1_exam")

async def ku_score(ctx: discord_slash.SlashContext):
    
    member = cpe35_server_user.get_item(Key={'id':ctx.author_id})['Item']
    try:
        member_score = cpe35_y1_exam.get_item(Key = {'id_ku': int(member['id_ku'])})['Item'] 
    except KeyError:
        await ctx.send('Unable to get score data.', delete_after=10)
        return
    
    em = discord.Embed(title = 'Computer Programming Midterm Quiz Score')
    em.add_field(name = 'Score', value = member_score['s1_q1_score'], inline=False)
    em.add_field(name = 'Percentage', value = member_score['s1_q1_percentage'], inline=False)
    em.add_field(name = 'Grade', value = member_score['s1_q1_grade'], inline=False)
    
    await ctx.send('Check your PM!', delete_after=10)
    await ctx.author.send(embed= em)
    

