import discord
from discord.ext import commands
import json
import asyncio
import requests

CONFIG = r'콘픽'

def load_config():
    with open(CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def save_config(config):
    with open(CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

config = load_config()
TOKEN = config.get("token")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def 도움말(ctx):
    message = (
        "1️⃣ 채팅: 채팅을 하려면 !채팅을 입력하세요\n"
        "2️⃣ 도구: 도구를 보려면 !도구를 입력하세요\n"
        "3️⃣ 설정: 설정을 변경하려면 !설정을 입력하세요\n"
    )
    await ctx.send(message)


@bot.command()
async def 채팅(ctx):
    message = (
        "1️⃣ 도배: 도배를 하려면 !도배 갯수 내용 을 입력하세요\n"
        "2️⃣ 청소: 청소를 하려면 !청소 갯수 를 입력하세요\n"
    )
    await ctx.send(message)

@bot.command()
async def 도배(ctx, count: int, *, message: str):
    if message.strip() == "":
        await ctx.send("빈 메시지는 보낼 수 없어요!")
        return
    for _ in range(count):
        await ctx.send(message)

@bot.command()
async def 청소(ctx, count: int):
    if isinstance(ctx.channel, discord.DMChannel):
        async for message in ctx.channel.history(limit=count+1):
            if message.author == ctx.author:
                await message.delete()
        await ctx.send(f"{count}개의 메시지를 삭제했습니다.")
        return

    deleted_messages = await ctx.channel.purge(limit=count+1, check=lambda m: m.author == ctx.author)
    deleted_count = len(deleted_messages) - 1
    await ctx.send(f"{deleted_count}개의 메시지를 삭제했습니다.", delete_after=5)



@bot.command()
async def 도구(ctx):
    message = (
        "1️⃣ 관리: 서버 관리 기능을 이용하려면 !관리 를 입력하세요\n"
        "2️⃣ ip: 아이피 기능을 이용하려면 !ip ip주소 를 입력하세요\n"
    )
    await ctx.send(message)

@bot.command()
async def 관리(ctx):
    if ctx.guild is None:
        await ctx.send("이 명령어는 서버에서만 사용할 수 있습니다.")
        return

    # 관리자 권한 확인
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("서버 관리 기능을 사용하기 위해서는 관리자 권한이 필요합니다.")
        return

    message = (
        "1️⃣ 밴: 밴하려면 !밴 유저멘션 을 입력하세요\n"
        "2️⃣ 추방: 추방하려면 !추방 유저멘션 을 입력하세요\n"
        "3️⃣ 별명: 별명을 변경하려면 !별명 유저멘션 새별명 을 입력하세요\n"
    )
    await ctx.send(message)

@bot.command()
async def 밴(ctx, member: discord.Member):
    if ctx.guild is None:
        await ctx.send("이 명령어는 서버에서만 사용할 수 있습니다.")
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("이 명령어를 사용하기 위해서는 관리자 권한이 필요합니다.")
        return
    await member.ban()
    await ctx.send(f"{member}님을 밴했습니다.")

@bot.command()
async def 추방(ctx, member: discord.Member):
    if ctx.guild is None:
        await ctx.send("이 명령어는 서버에서만 사용할 수 있습니다.")
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("이 명령어를 사용하기 위해서는 관리자 권한이 필요합니다.")
        return
    await member.kick()
    await ctx.send(f"{member}님을 추방했습니다.")

@bot.command()
async def 별명(ctx, member: discord.Member, nickname: str):
    if ctx.guild is None:
        await ctx.send("이 명령어는 서버에서만 사용할 수 있습니다.")
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("이 명령어를 사용하기 위해서는 관리자 권한이 필요합니다.")
        return
    await member.edit(nick=nickname)
    await ctx.send(f"{member}님의 별명을 {nickname}로 변경했습니다.")

@bot.command()
async def ip(ctx, address: str):
    try:
        response = requests.get(f'http://ip-api.com/json/{address}')
        data = response.json()

        if data.get('status') == 'success':
            ip_address = f"> **IP 주소: {data['query']}**"
            country = f"> **나라: {data['country']}**"
            city = f"> **도시: {data['city']}**"
            zip_code = f"> **우편번호: {data['zip']}**"
            isp = f"> **ISP: {data['isp']}**"
            map = f"> **지도: [클릭하여 구글지도로 이동하기](https://google.com/maps/place/{address})**"

            message = f"## IP 정보\n{ip_address}\n{country}\n{city}\n{zip_code}\n{isp}\n{map}"

            await ctx.send(message)
        else:
            await ctx.send("주소에 대한 정보를 찾을 수 없습니다.")
    except Exception as e:
        await ctx.send(f"IP 조회 중 오류가 발생했습니다: {e}")

@bot.command()
async def 설정(ctx):
    message = (
        "1️⃣ 접두사 변경: 접두사를 변경하려면 !접두사 새접두사 을 입력하세요\n"
        "2️⃣ 내 별명 변경: 본인의 별명을 변경하려면 !내별명 변경할별명 을 입력하세요\n"
    )
    await ctx.send(message)

@bot.command()
async def 접두사(ctx, new_prefix: str):
    bot.command_prefix = new_prefix
    await ctx.send(f"접두사가 '{new_prefix}'로 변경되었습니다.")

@bot.command()
async def 내별명(ctx, new_nickname: str):
    await ctx.author.edit(nick=new_nickname)
    await ctx.send(f"본인의 별명을 '{new_nickname}'으로 변경했습니다.")

if __name__ == '__main__':
    bot.run(TOKEN, bot=False)
