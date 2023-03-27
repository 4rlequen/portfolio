import discord
import string
import json
import sqlite3
import asyncpraw
import asyncio
import config
from discord.ext import commands

TOKEN='MTAzNjY5NDYyNzM3MTE5MjM3MA.Gyj4Tq.Dap728jlRWtDinidmYpQARNmPmMjhI6f9i_oss'


base = sqlite3.connect('server.db')
base.execute('CREATE TABLE IF NOT EXISTS warning(userid INT, count INT, mute INT)')
cursor = base.cursor()


base.commit()
bot=commands.Bot(command_prefix='/',intents=discord.Intents.all())
reddit = asyncpraw.Reddit(client_id =config.settings['ID'],client_secret =config.settings['SECRET'],user_agent='chat_bot')
posts = []
TIMEOUT = 5
NAME ='memes'
LIMIT = 1

@bot.event
async def on_ready():
    print('РАБОТАЕМ!')
@bot.command()
async def info(ctx,msg=None):
    if msg==None:
        await ctx.send('Этот бот следит за порядком в чате')
    elif msg=='команды':
        await ctx.send('unmute- снятие заглушения \n mute- заглушение\n info_w- информвция об нарушениях\n clear-чистка сообщений')

# @bot.command()
# async def start(ctx):
#     global channel
#     for ch in bot.get_guild(ctx.author.guild.id).channels:
#         if ch.name == 'основной':
#             channel = ch
#     while True:
#         await asyncio.sleep(TIMEOUT)
#         posts_submissions = await reddit.subreddit(NAME)
#         posts_submissions = posts_submissions.new(limit=LIMIT)
#         item = await posts_submissions.__anext__()
#         if item.title not in posts:
#             posts.append(item.title)
#             await channel.send(item.url)

@bot.event
async def on_message(message):
    global cursor, base
    slova={i.lower().translate(str.maketrans("","",string.punctuation)) for i in message.content.split(' ')}
    zs=set(json.load(open('cenz.json')))
    if slova.intersection(zs) != set():
        await message.channel.send("Такое писать нельзя")
        await message.delete()
        cursor.execute(f'SELECT* FROM warning WHERE userid={message.author.id}')
        warning=cursor.fetchone()[1]
        base.commit()
        if warning==None:
            await message.channel.send(f'{message.author} Первое предупреждение!')
            cursor.execute(f'INSERT INTO warning VALUES({message.author.id},1)')
            base.commit()
        elif warning==1:
            await message.channel.send(f'{message.author} второе предупреждение!')
            cursor.execute(f'UPDATE warning SET count=={2} WHERE userid=={message.author.id}')
            base.commit()
        elif warning==2:
            await message.channel.send(f'{message.author} Бан!')
            cursor.execute(f'UPDATE warning SET count=={3} WHERE userid=={message.author.id}')
            base.commit()
            await message.author.ban(reason='С третьего раза не понимаешь')



    await bot.process_commands(message)
@bot.command()
async def info_w(ctx,member:discord.Member):
    global cursor,base
    cursor.execute(f'SELECT* FROM warning WHERE userid=={member.id}')
    count=cursor.fetchone()[1]
    base.commit()
    if count==None:
        await ctx.send(f'У {member.name} 0 нарушений')
    else:
        await ctx.send(f'У {member.name} {count} нарушений')



@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=100):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)
@bot.command()
async def send_member(ctx,member:discord.Member):
    await member.send(f'{member.name} привет от {ctx.author.name}')

@bot.event
async def on_member_join(member):
    global cursor,base
    for i in bot.get_guild(member.guild.id).channels:
        if i.name == "основной":
            await bot.get_channel(i.id).send(f"Здравствуй {member.name}")
    talk=discord.utils.get(member.guild.roles,name="talk")
    mute=discord.utils.get(member.guild.roles,name="mute")
    cursor.execute((f'INSERT INTO warning VALUES({member.id},0,0)'))
    cursor.execute(f'SELECT* FROM warning WHERE userid={member.id}')
    users_mute = cursor.fetchone()[2]
    base.commit()
    if users_mute==None:
        cursor.execute(f'INSERT INTO warning VALUES({member.id},0,0)')
        base.commit()
        await member.add_roles(talk)
    elif users_mute==0:
        await member.add_roles(talk)
    else:
        await member.remove_roles(talk)
        await member.add_roles(mute)



@bot.event
async def on_member_remove(member):
    for i in bot.get_guild(member.guild.id).channels:
        if i.name =="основной":
            await bot.get_channel(i.id).send(f"Прощай {member.name}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx,member:discord.Member):
    talk = discord.utils.get(member.guild.roles, name="talk")
    mute_role=discord.utils.get(member.guild.roles,name='mute')
    await member.remove_roles(talk)
    await member.add_roles(mute_role)
    await ctx.send(f'У {member.name} забирают права')
    cursor.execute(f'UPDATE warning SET mute == 1 WHERE userid=={member.id}')
    base.commit()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx,member:discord.Member):
    talk = discord.utils.get(member.guild.roles, name="talk")
    mute_role = discord.utils.get(member.guild.roles, name='mute')
    await member.remove_roles(mute_role)
    await member.add_roles(talk)
    cursor.execute(f'UPDATE warning SET mute == 0 WHERE userid=={member.id}')
    base.commit()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unban(ctx,member:discord.Member):
    cursor.execute(f'UPDATE warning SET count == 0 WHERE userid=={member.id}')
    base.commit()



#bot.run(token='MTAzNjY5NDYyNzM3MTE5MjM3MA.Gyj4Tq.Dap728jlRWtDinidmYpQARNmPmMjhI6f9i_oss')
bot.run(config.settings['TOKEN'])