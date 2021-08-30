import platform
import discord
from discord.ext.commands import Bot
from src.utils.config import Prefix
from src.format.code import formatCode, formatCode_emb
from src.utils.member import getNick
from datetime import datetime

from src.utils.codechannel import addGuild
GUILD_IDS = None
ADMIN_ID = 186315352026644480


class TuanAraiMaiRoo(Bot):

    def __init__(self):
        activity = discord.Activity(type=discord.ActivityType.competing, name='the universe')
        Bot.__init__(self,command_prefix=Prefix,
                   intents=discord.Intents.all(),
                   case_insensitive=True,
                   activity=activity,
                   status=discord.Status.online)
    
    async def on_ready(self):
        global GUILD_IDS
        print(datetime.now())
        GUILD_IDS = [guild.id for guild in self.guilds]
        GUILD_NAMES = [guild.name for guild in self.guilds]
        print(GUILD_NAMES)
        me = await self.fetch_user(ADMIN_ID)
        await me.send(f"Running {self.user.name} on\n{platform.uname()}")
    
    async def on_guild_join(self,guild):
        global GuildData
        global GuildIDs
        if guild.id not in GuildIDs:
            addGuild(guild.id)
            print(f'added {guild.id} to guild db')
            from src.utils.codechannel import GuildData, GuildIDs

    async def on_message(self, msg:discord.Message):
        global GuildData, GuildIDs
        try:
            if msg.guild.id not in GuildIDs:
                addGuild(msg.guild.id)
                print(f'added {msg.guild.id} to guild db')
                from utils.codechannel import GuildData, GuildIDs

            channel = msg.channel
            guilddata = GuildData(msg.guild.id)

            if channel.id in guilddata.codechannel_ids:
                language = guilddata.channeldata(channel.id)['lang']

                if msg.author.bot or msg.content[0] in ['_', '*', '`']:
                    return

                await TuanAraiMaiRoo.send_fmc(msg, language)

                await msg.delete()
                return
        except:
            pass
    
    @staticmethod
    async def send_fmc(msg: discord.Message, language: str):
        if msg.content[:2] in '-e':
            fmc = formatCode_emb(msg, language, msg.content[2:])
            if type(fmc) == list:
                SCfst = '\n'.join(fmc[0])
                pfp = msg.author.avatar_url
                embed = discord.Embed()
                embed.set_thumbnail(url=pfp)
                embed.add_field(
                    name='Code', value=f"""By {getNick(msg.author)}```{language}\n{SCfst}\n```""")
                for count, code in enumerate(fmc[1:], start=1):
                    SCrest = '\n'.join(code)
                    embed.add_field(
                        name=f'#continue {count}', value=f"""```{language}\n{SCrest}\n```""", inline=False)
                await msg.channel.send(embed=embed)
            else:
                await msg.channel.send(embed=fmc)
        else:
            fmc = formatCode(msg, language, msg.content)
            if type(fmc) == list:
                SCfst = '\n'.join(fmc[0])
                await msg.channel.send(f"""By {getNick(msg.author)}```{language}\n{SCfst}\n```""")
                for code in fmc[1:]:
                    SCline = '\n'.join(code)
                    await msg.channel.send(f"""```{language}\n{SCline}\n```""")
            else:
                await msg.channel.send(formatCode(msg, language, msg.content))