from discord_slash import SlashContext
from discord import Embed
from src.utils import aws


colors = {'fail': 0xb01111,
          'pass': 0x37e407}


async def ku_score(ctx: SlashContext):
    
    try:
        member = aws.cpe35_user_table.get_item(Key={'id':ctx.author_id})['Item']
        member_score = aws.cpe35_y1_exam_table.get_item(Key = {'id_ku': int(member['id_ku'])})['Item'] 
    except KeyError:
        await ctx.send('Unable to get score data.', delete_after=10)
        return
    
    em = Embed(title = 'Computer Programming Midterm Quiz Score')
    em.add_field(name = 'Score', value = member_score['s1_q1_score'], inline=False)
    em.add_field(name = 'Percentage', value = member_score['s1_q1_percentage'], inline=False)
    em.add_field(name = 'Grade', value = member_score['s1_q1_grade'], inline=False)
    
    await ctx.send('Check your PM!', delete_after=10)
    await ctx.author.send(embed= em)
    

