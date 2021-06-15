import discord
from discord.ext import commands
from PingPongTool import PingPong
from random import randint

def RandomColor():
    return randint(0, 0xFFFFFF)

TOKEN = "ODM5MTM3ODg4MzY4NDU5Nzk2.YJFSDw.nyLQH9YSXqbjaxS6gY_4FULX9zo"
Authorization = "Basic a2V5Ojg4ZGQ2MzM3ODNmZGIzZjYyNTE1OWNhZDUxNzMwNjVk"
URL = "https://builder.pingpong.us/api/builder/5e628acfe4b04226d4599711/integration/v0.2/custom/{sessionId}"

bot = commands.Bot(command_prefix=['!&@!*!&@^*&!$!(*@))(**!$&(*!@*', '뉴하야 '])
Ping = PingPong(URL, Authorization)

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')

@bot.listen()
async def on_command_error(ctx, error):
    if type(error) is commands.errors.CommandNotFound:
        data = await Ping.Pong(ctx.author.id, ctx.message.content, NoTopic=False)
        embed = discord.Embed(
            title=" ",
            description=data['text'],
            color=0xd72a71
        )
        embed.set_footer(text="뉴하진윤 개발")
        if data['image']:
            embed.set_image(url=data['image'])
        await ctx.send(embed=embed)


@bot.command(name="따라해핑퐁")
async def Echo(ctx, *, text: str):
    await ctx.send(text)

bot.run('ODQ4MTExMDg4NTQ1MTY5NDA4.YLH3AA.Jx3aTCO9fLylREr0O-pjn9v2WsQ')