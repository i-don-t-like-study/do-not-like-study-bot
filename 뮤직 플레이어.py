import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

bot = commands.Bot(command_prefix='>')
client = discord.Client()

user = [] #유저가 입력한 노래 정보임 ㅅㄱ
musictitle = [] 
song_queue = []
musicnow = []

number = 1

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = r"D:\develope\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx)) 

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())

def again(ctx, url):
    global number
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if number:
        with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        if not vc.is_playing():
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: again(ctx, url))

#-----------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">도움 을 입력해 도움 받기"))

@bot.command()
async def 따라해(ctx, *, text):
    await ctx.send(text)

@bot.command()
async def 나무위키(ctx, *, text):
    await ctx.send("https://namu.wiki/w/" +text)

@bot.command()
@commands.has_role('ADMIN')
async def 공지(ctx, *, text):
  channel = bot.get_channel(854346073903857684)
  await channel.send(embed = discord.Embed(title=ctx.message.author.name +"님의 공지",description=text, color = 0x00ff00))
  await ctx.send(embed = discord.Embed(title='공지 성공적으로 올려짐',description=text, color = 0x00ff00))

@bot.command()
async def 서버인원수(ctx):
    await ctx.send(ctx.guild.member_count)

#-----------------------------------------------------------------------------------------------------------------
@bot.command()
async def 들어와(ctx):
    await ctx.send("`이제는 그냥 재생만 해도 들어옵니다 따라서 이 기능은 곧 삭제됩니다.`")
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성채널에 접속해주세요")

@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("그 채널에 접속해있지 않아요")

@bot.command()
async def 도움(ctx):
    await ctx.send(embed = discord.Embed(title='도움말',description="""
접두어 =
\> = 봇 명령어
클러야 = 인공지능 대화 명령어
\n>도움 -> 공부시러봇의 모든 명령어를 볼 수 있습니다.
>따라해 [메세지] -> 말을 따라하는 앵무새 공부시러봇! (악용시 처벌)
>나무위키 [찾아볼것] -> 나무위키 링크를 생성합니다
>서버인원수 -> 서버인원수를 확인합니다
\n>들어와 -> 공부시러봇을 자신이 속한 채널로 부릅니다.
\n>나가 -> 공부시러봇을 자신이 속한 채널에서 내보냅니다.
(목록재생에서는 사용할 수 없습니다.)
\n>재생 [노래이름/노래유튜브링크] -> 공부시러이 노래를 검색해 틀어줍니다. + (자동으로 다음 목록에 추가됩니다)
\n>멈춰 -> 현재 재생중인 노래를 끕니다.
>일시정지 -> 현재 재생중인 노래를 일시정지시킵니다.
>다시재생 -> 일시정지시킨 노래를 다시 재생합니다.
\n>지노 -> 지금 재생되고 있는 노래의 제목을 알려줍니다.
\n>목록 -> 이어서 재생할 노래목록을 보여줍니다.
>목록재생 -> 목록에 추가된 노래를 재생합니다.
>목록초기화 -> 목록에 추가된 모든 노래를 지웁니다.
\n>대기열추가 [노래] -> 노래를 대기열에 추가합니다.
>대기열삭제 [숫자] -> 대기열에서 입력한 숫자에 해당하는 노래를 지웁니다.""", color = 0x00ff00))

@bot.command()
async def URL재생(ctx, *, url):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
           await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성채널에 접속해주세요")

    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "둠칫둠칫", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다! (다음 재생목록에 추가는 검색 재생만 가능합니다. 이건 나중에~)")

@bot.command()
async def 재생(ctx, *, msg):
    await ctx.send("`이 기능은 검색으로 URL재생보다 엄청나게 느리게 로딩됩니다. 빠른 재생을 원하시면 >URL재생 (유튜브주소) 를 입력해주세요`")
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성채널에 접속해주세요")

    if not vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = "D:\develope\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query="+msg)
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "검색한 둠칫둠칫", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        user.append(msg)
        result,URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send("이미 노래가 재생 중이라 " + result + "을(를) 재생목록에 추가했어요!")

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "끼이익!", description = musicnow[0] + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("벌써 일시정지 또는 안틀어져 있는걸요?")

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("벌써 재생중이거나 또는 안틀어져 있는걸요?")
    else:
         await ctx.send(embed = discord.Embed(title= "발사!", description = musicnow[0]  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command()
async def 멈춰(ctx):
    if vc.is_playing():
        vc.stop()
        global number
        number = 0
        await ctx.send(embed = discord.Embed(title= "끼이이이이익!!", description = musicnow[0]  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("벌써 멈춰있거나 또는 안틀어져 있는걸요?")

@bot.command()
async def 지노(ctx):
    if not vc.is_playing():
        await ctx.send("노래가 재생중이지 않아요")
    else:
        await ctx.send(embed = discord.Embed(title = "잠시만요... 1..2...3..", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))

@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했어요!")

@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화되었습니다. 이제 노래를 등록해볼까요?""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

@bot.command()
async def 목록재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")

bot.run('키')
