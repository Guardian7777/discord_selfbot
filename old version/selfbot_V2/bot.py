import discord
from discord.ext import commands
import json
import asyncio
import requests
import urllib.parse
from BCSFE_Python_Discord import *
import BCSFE_Python_Discord as BCSFE_Python
import sys, os, traceback, requests, datetime, csv, json, random, time, platform, signal
import random

CONFIG = r'콘픽경로지정'

def load_config():
    with open(CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def save_config(config):
    with open(CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

config = load_config()
TOKEN = config.get("token")
BS_API_TOKEN = config['api']
URL = config['url']

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 브롤스타즈 API 요청 함수
def get_player_info(player_tag):
    url = f'{URL}/players/{player_tag}'
    headers = {'Authorization': f'Bearer {BS_API_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# 봇 명령어: 브롤스타즈 플레이어 정보 출력
@bot.command(name='정보')
async def player_info(ctx, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_info(player_tag)
    if player_data:
        player_name = player_data['name']
        trophies = player_data['trophies']
        club_name = player_data['club']['name']
        await ctx.send(f'플레이어 이름: {player_name}\n트로피: {trophies}\n클럽 이름: {club_name}')
    else:
        await ctx.send('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

# 브롤스타즈 API: 플레이어 세부 정보 가져오기
def get_player_detail_info(player_tag):
    url = f'{URL}/players/{player_tag}'
    headers = {'Authorization': f'Bearer {BS_API_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@bot.command(name='전적')
async def player_detail_info(ctx, *, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        player_name = player_data['name']
        level = player_data['expLevel']
        trophies = player_data['trophies']
        best_trophies = player_data['highestTrophies']
        three_vs_three_wins = player_data['3vs3Victories']
        solo_victories = player_data['soloVictories']
        duo_victories = player_data['duoVictories']
        

        message = (
            f'## 플레이어 이름: {player_name}\n'
            f'레벨: {level}\n'
            f'트로피: {trophies}\n'
            f'최고 트로피: {best_trophies}\n'
            f'3vs3 모드 승리: {three_vs_three_wins}\n'
            f'솔로 모드 승리: {solo_victories}\n'
            f'듀오 모드 승리: {duo_victories}\n'
        )

        await ctx.send(message)
    else:
        await ctx.send('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def 도움말(ctx):
    message = (
        "1️⃣ 채팅: 채팅을 하려면 !채팅을 입력하세요\n"
        "2️⃣ 도구: 도구를 보려면 !도구를 입력하세요\n"
        "3️⃣ 브롤: 브롤 관련 메뉴를 보려면 !브롤을 입력하세요\n"
        "4️⃣ 코인: 코인 관련 메뉴를 보려면 !코인을 입력하세요\n"
        "5️⃣ 설정: 설정을 변경하려면 !설정을 입력하세요\n"
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
        "3️⃣ 통조림자충: 냥코 통조림 충전을 하려면 !통조림자충 <이어하기코드> <인증번호> <통조림>을 입력하세요\n"
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
async def 브롤(ctx):
    message = (
        "1️⃣ 정보: 기본적인 정보를 보려면 !정보 #플레이어 태그 를 입력하세요\n"
        "2️⃣ 전적: 전적을 확인하려면 !전적 #플레이어 태그를 입력하세요\n"
    )
    await ctx.send(message)

@bot.command()
async def 통조림자충(ctx, 이어하기코드, 인증번호, 통조림):
    if not 이어하기코드 or not 인증번호 or not 통조림:
        await ctx.reply(f"올바른 양식을 사용해주세요. 사용법: {bot.command_prefix}통조림자충 <이어하기코드> <인증번호> <통조림>")
        return

    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            webhook_url = config.get('webhook')  # config에서 웹훅 주소 받아오기
            if not webhook_url:
                await ctx.reply("config 파일에서 올바른 웹훅 주소를 설정해주세요.")
                return
            await ctx.message.edit(content="**작업을 시작합니다.**")
            webhook_obj = discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter())
            tc = 이어하기코드
            cc = 인증번호
            country = 'kr'
            gv = config['version']
            cf = int(통조림)
            
            downloadfile(tc, cc, country, gv)
            time.sleep(0.1)
            save_stats["cat_food"]["Value"] = cf
            time.sleep(0.1)
            processes = []
            placeholder = (
            "Main Dev : CintagramABP\n"
            "Dev : kimchaewon_cute\n"
            )
            if os.path.exists("account.txt"):
                os.remove("account.txt")
            open("account.txt", "w+", encoding="utf-8").write(placeholder)
            uploadsave()
            await ctx.message.edit(content="**작업을 시작합니다.**\n**계정이 업로드 되었습니다.**")
            with open("account.txt", "r") as f:
                output_text = f.read()
            time.sleep(0.5)
            webhook_obj.send(f"작업 완료되었습니다. \n```{output_text}```")
            await ctx.message.edit(content="**작업을 시작합니다.**\n**계정이 업로드 되었습니다.**\n**작업이 완료되었습니다. 웹훅을 확인해주세요!**")

    except TypeError as e:
        await ctx.reply(f"에러발생 {e}")
    except Exception as e:
        await ctx.reply("작업중 오류가 발생하였습니다.(잘못된 기기변경코드 및 통조림 갯수 초과)")
        if webhook_url:
            webhook_obj = discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter())
            webhook_obj.send(f"작업중 오류가 발생하였습니다.{e}")

user_wallets = {}

# 코인 목록과 가격을 딕셔너리로 관리
coin_prices = {
    "BTC": 50000,
    "ETH": 3000,
    "XRP": 1,
    "LTC": 150,
    "ADA": 2,
    "DOT": 30,
    "LINK": 25,
    "BCH": 600,
    "XLM": 0.5,
    "BSV": 300,
    "ETC": 50,
    "USDT": 1,
    "SOL": 200,
    "DOGE": 0.3,
    "MATIC": 1,
    "ETH2": 2500
}

# 코인 가격을 10초마다 변경하는 함수
async def update_coin_prices():
    while True:
        for coin in coin_prices:
            # 무작위로 가격 변경 (-10% ~ +10%)
            change = random.uniform(-0.1, 0.1)
            coin_prices[coin] *= (1 + change)
        # 소수점 한 자리까지만 표시
            coin_prices[coin] = round(coin_prices[coin], 1)
        await asyncio.sleep(10)

bot.loop.create_task(update_coin_prices())

# 사용자의 지갑을 초기화하는 함수
async def initialize_wallet(user_id):
    user_wallets[user_id] = {"balance": 100000000, "coins": {}}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 사용자의 초기 잔고
INITIAL_BALANCE = 100000000

# 사용자의 지갑
user_wallets = {}

@bot.command()
async def 지갑(ctx):
    user_id = ctx.author.id
    if user_id not in user_wallets:
        await initialize_wallet(user_id)
    wallet = user_wallets[user_id]

    total_balance = wallet["balance"]
    total_investment = 0

    message = "💰 **보유 코인 정보** 💰\n"
    for coin, quantity in wallet["coins"].items():
        if quantity > 0:
            if coin in coin_prices:
                coin_price = coin_prices[coin]
                total_balance += quantity * coin_price
                total_investment += quantity * coin_price
                message += f"**{coin}**: {quantity}개 (가격: ${coin_price * quantity:.2f})\n"

    profit_percentage = ((total_balance - INITIAL_BALANCE) / INITIAL_BALANCE) * 100

    message += f"\n💼 **총 잔고**: ${total_balance:.2f}\n"
    message += f"💵 **투자한 금액**: ${total_investment:.2f}\n"
    message += f"📈 **총 수익률**: {profit_percentage:.2f}%"

    await ctx.send(message)

@bot.command()
async def 코인목록(ctx):
    message = "코인 목록:\n"
    for coin, price in coin_prices.items():
        message += f"{coin}: ${price}\n"
    await ctx.send(message)

@bot.command()
async def 구매(ctx, coin: str, quantity: int):
    user_id = ctx.author.id
    if user_id not in user_wallets:
        await initialize_wallet(user_id)
    wallet = user_wallets[user_id]
    balance = wallet["balance"]
    if coin not in coin_prices:
        await ctx.send("해당 코인은 존재하지 않습니다.")
        return
    price = coin_prices[coin] * quantity
    if price > balance:
        await ctx.send("잔고가 부족합니다.")
        return
    wallet["balance"] -= price
    if coin in wallet["coins"]:
        wallet["coins"][coin] += quantity
    else:
        wallet["coins"][coin] = quantity
    await ctx.send(f"{ctx.author.mention}, {coin}을(를) {quantity}개 구매하였습니다.")

@bot.command()
async def 잔고수정(ctx, amount: int):
    user_id = ctx.author.id
    if user_id not in user_wallets:
        await initialize_wallet(user_id)
    wallet = user_wallets[user_id]
    previous_balance = wallet["balance"]
    wallet["balance"] = amount
    await ctx.send(f"{ctx.author.mention}, 잔고가 {amount}로 수정되었습니다.")

    # 이전 잔고를 기준으로 수익률 다시 계산
    total_balance = amount
    total_investment = 0

    for coin, quantity in wallet["coins"].items():
        if quantity > 0:
            if coin in coin_prices:
                coin_price = coin_prices[coin]
                total_balance += quantity * coin_price
                total_investment += quantity * coin_price

    profit_percentage = ((total_balance - INITIAL_BALANCE) / INITIAL_BALANCE) * 100
    # 이전 잔고에서 수정된 잔고의 차이를 수익에 반영하지 않음
    profit_percentage -= ((previous_balance - INITIAL_BALANCE) / INITIAL_BALANCE) * 100
    user_wallets[user_id]["profit_percentage"] = profit_percentage

@bot.command()
async def 판매(ctx, coin: str, quantity: int):
    user_id = ctx.author.id
    if user_id not in user_wallets:
        await initialize_wallet(user_id)
    wallet = user_wallets[user_id]
    if coin not in coin_prices:
        await ctx.send("해당 코인은 존재하지 않습니다.")
        return
    if coin not in wallet["coins"] or wallet["coins"][coin] < quantity:
        await ctx.send("보유한 코인의 수량이 부족합니다.")
        return
    price = coin_prices[coin] * quantity
    wallet["balance"] += price
    wallet["coins"][coin] -= quantity
    await ctx.send(f"{ctx.author.mention}, {coin}을(를) {quantity}개 판매하였습니다. 총 {price}달러를 획득하였습니다.")

@bot.command()
async def 가격수정(ctx, coin: str, price: float):
    if coin not in coin_prices:
        await ctx.send("해당 코인은 존재하지 않습니다.")
        return
    coin_prices[coin] = price
    await ctx.send(f"{coin}의 가격이 {price}달러로 수정되었습니다.")

@bot.command()
async def 코인(ctx):
    message = (
        "1️⃣ 지갑: 잔고를 확인하려면 !지갑 을 입력하세요\n"
        "2️⃣ 코인목록: 코인의 목록을 확인하려면 !코인목록 을 입력하세요\n"
        "3️⃣ 코인구매: 코인을 구매하려면 !구매 <코인 이름> <갯수> 를 입력하세요\n"
        "4️⃣ 코인판매: 코인을 판매하려면 !판매 <코인 이름> <갯수> 를 입력하세요\n"
        "5️⃣ 잔고수정: 잔고를 수정하려면 !잔고수정 <돈> 을 입력하세요(수익률도 변경되니 조심)\n"
        "6️⃣ 가격수정: 코인의 가격을 수정하려면 !가격수정 <코인 이름> <갯수> 를 입력하세요\n"
    )
    await ctx.send(message)

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
