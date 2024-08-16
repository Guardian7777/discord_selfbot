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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
import pytz
from googlesearch import search
from googletrans import Translator
import pyupbit
import math

CONFIG = r"콘픽경로" # 만약 A-SHELL 에서 구동하면 앞에 r 빼고 올려둔 파일 다 A-SHELL 폴더에 넣고 "./config.json" 으로 바꾸셈

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
prefix = config["prefix"]
TAG = config["tag"]
WEB = config["mywebhook"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=config["prefix"], self_bot=True, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def 핑(ctx):
    await ctx.reply(f"퐁! 지연시간: {round(bot.latency * 1000)} ms")

@bot.command()
async def 도움말(ctx):
    prefix = config["prefix"]
    message = (
        "## 도움말\n"
        f"> **1️⃣ 채팅: 채팅을 하려면 {prefix}채팅을 입력하세요**\n"
        f"> **2️⃣ 도구: 도구를 보려면 {prefix}도구를 입력하세요**\n"
        f"> **3️⃣ 브롤: 브롤 관련 메뉴를 보려면 {prefix}브롤을 입력하세요**\n"
        f"> **4️⃣ 코인: 코인 관련 메뉴를 보려면 {prefix}코인을 입력하세요**\n"
        f"> **5️⃣ 설정: 설정을 변경하려면 {prefix}설정을 입력하세요**\n"
    )
    await ctx.reply(message)

# 본인 메시지 관리 기능, 밈 보내기 기능 있음 원하는 밈 디코로 보내주면 추가함
@bot.command()
async def 채팅(ctx):
    prefix = config["prefix"]
    message = (
        "## 채팅 메뉴\n"
        f"> **1️⃣ 도배: 도배를 하려면 {prefix}도배 갯수 내용 을 입력하세요**\n"
        f"> **2️⃣ 청소: 청소를 하려면 {prefix}청소 갯수 를 입력하세요**\n"
        f"> **3️⃣ 릭롤: {prefix}릭롤**\n"
        f"> **4️⃣ 랜덤짤: 랜덤짤을 보내려면 {prefix}랜덤짤 을 입력하세요**\n"
        f"> **5️⃣ 강화: 아이템을 강화하려면 {prefix}강화 강화할 아이템 을 입력하세요**\n"
    )
    await ctx.reply(message)

@bot.command()
async def 도배(ctx, count: int, *, message: str):
    if message.strip() == "":
        await ctx.reply("빈 메시지는 보낼 수 없어요!")
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
async def 릭롤(ctx):
    await ctx.send('https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713')

# 랜덤짤 링크 리스트
random_jjal_links = [
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224510",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224522",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224538",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224523",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224532",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224505",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224521",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224501",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224499",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224500",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-mc%EB%AC%B4%ED%98%84-%EB%AC%B4%ED%98%84-%EB%86%88%ED%98%84-gif-20749558",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224512",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224517",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224504",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224539",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224516",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819009",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224511",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224502",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819011",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224519",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224514",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-speech-gif-14501752",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224530",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819007",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-2275462757071994202",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224527",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224536",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224506",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819006",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224508",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224533",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819002",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224531",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819008",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224524",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224509",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819001",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224515",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819004",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224537",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819005",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-21819003",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224528",
    "https://tenor.com/view/%EB%85%B8%EB%AC%B4%ED%98%84-gif-22224518"
]

# 사용시 주의 필요
@bot.command()
async def 랜덤짤(ctx):
        random_jjal = random.choice(random_jjal_links)
        await ctx.reply(random_jjal)

# 강화할 아이템과 초기 강화 수준 설정
enhance_items = {}

# 강화 기록 관리
user_enhance_records = {}

@bot.command()
async def 강화(ctx, item_name: str):
    user_id = ctx.author.id
    
    # 강화 기록 초기화
    if user_id not in user_enhance_records:
        user_enhance_records[user_id] = {}
    
    # 아이템 초기화
    if item_name not in enhance_items:
        enhance_items[item_name] = {"enhance_level": 0}
    
    # 강화 기록 초기화
    if item_name not in user_enhance_records[user_id]:
        user_enhance_records[user_id][item_name] = {"enhance_level": 0}

    current_level = user_enhance_records[user_id][item_name]["enhance_level"]
    
    # 강화 시도
    success_rate = get_success_rate(current_level)
    fail_chance = get_fail_chance(current_level)

    if random.random() < success_rate:
        # 강화 성공
        user_enhance_records[user_id][item_name]["enhance_level"] += 1
        await ctx.send(f"{ctx.author.mention}, {item_name}을(를) 강화하여 {current_level + 1}강이 되었습니다!")
    else:
        # 강화 실패
        if current_level > 0:
            user_enhance_records[user_id][item_name]["enhance_level"] -= 1
            await ctx.send(f"{ctx.author.mention}, {item_name} 강화 실패! {current_level - 1}강으로 강화 레벨이 감소하였습니다.")
        else:
            await ctx.send(f"{ctx.author.mention}, {item_name} 강화 실패! 최하 강화 레벨입니다.")

        # 10강 이상일 때 터질 확률 추가
        if current_level >= 10 and random.random() < fail_chance:
            user_enhance_records[user_id][item_name]["enhance_level"] = 0
            await ctx.send(f"{ctx.author.mention}, {item_name} 강화 실패로 인해 아이템이 터졌습니다. 강화 레벨이 초기화되었습니다.")

def get_success_rate(level):
    # 초기 성공 확률 설정
    success_rates = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55]
    if level < len(success_rates):
        return success_rates[level]
    else:
        return success_rates[-1]  # 최대 레벨 이후는 마지막 확률 유지

def get_fail_chance(level):
    # 강화 실패 시 터질 확률 설정
    fail_chances = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
    if level >= 10:
        if level - 10 < len(fail_chances):
            return fail_chances[level - 10]
        else:
            return fail_chances[-1]  # 최대 확률 유지
    else:
        return 0.0

@bot.command()
async def 강화목록(ctx):
    user_id = ctx.author.id
    
    if user_id not in user_enhance_records or not user_enhance_records[user_id]:
        await ctx.send("강화한 아이템이 없습니다.")
        return
    
    message = f"{ctx.author.mention}의 강화 목록:\n"
    for item_name, record in user_enhance_records[user_id].items():
        message += f"{item_name}: {record['enhance_level']}강\n"
    
    await ctx.send(message)

# 각종 도구
@bot.command()
async def 도구(ctx):
    prefix = config["prefix"]
    message = (
        "## 도구 메뉴\n"
        f"> **1️⃣ 관리: 서버 관리 기능을 이용하려면 {prefix}관리 를 입력하세요**\n"
        f"> **2️⃣ ip: 아이피 기능을 이용하려면 {prefix}ip ip주소 를 입력하세요**\n"
        f"> **3️⃣ 통조림자충: 냥코 통조림 충전을 하려면 {prefix}통조림자충 <이어하기코드> <인증번호> <통조림>을 입력하세요**\n"
        f"> **4️⃣ 구글: 구글 검색을 하시려면 {prefix}구글 내용 을 입력하세요**\n"
        f"> **5️⃣ 홍보: 홍보 기능을 이용하시려면 {prefix}홍보 를 입력하세요**\n" # config.json에 있는 promotion에 링크나 내용 작성
        f"> **6️⃣ 웹훅: 웹훅 명령어를 보시려면 {prefix}웹훅명령어 를 입력하세요**\n"
        f"> **7️⃣ 번역: 원하는 언어로 번역하려면 {prefix}번역 번역할 언어 번역할 문장 을 입력하세요**\n"
    )
    await ctx.reply(message)

# 서버에서 관리자 권한 있을 경우에만 사용 가능함
@bot.command()
async def 관리(ctx):
    if ctx.guild is None:
        await ctx.reply("이 명령어는 서버에서만 사용할 수 있습니다.")
        return

    # 관리자 권한 확인
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply("서버 관리 기능을 사용하기 위해서는 관리자 권한이 필요합니다.")
        return

    message = (
        "## 서버관리자 전용\n"
        f"> **1️⃣ 밴: 밴하려면 {prefix}밴 유저멘션 을 입력하세요**\n"
        f"> **2️⃣ 추방: 추방하려면 {prefix}추방 유저멘션 을 입력하세요**\n"
        f"> **3️⃣ 별명: 별명을 변경하려면 {prefix}별명 유저멘션 새별명 을 입력하세요**\n"
        f"> **4️⃣ 역할 생성/삭제: 역할을 생성 또는 삭제하려면 {prefix}역할 생성/제거 역할 이름 을 입력하세요 **\n"
        f"> **5️⃣ 역할 부여/회수: 역할을 부여 또는 회수하려면 {prefix}부여/회수 역할 이름 을 입력하세요**\n"
        f"> **6️⃣ 티켓 생성/삭제: 티켓을 생성 또는 삭제하려면 {prefix}티켓 생성/삭제 유저멘션 을 입력하세요 **\n"
        f"> **7️⃣ 티켓 열기/닫기: 티켓을 열거나 닫으려 {prefix}티켓 열기/닫기 유저멘션 을 입력하세요**\n"
    )
    await ctx.reply(message)

@bot.command()
async def 밴(ctx, member: discord.Member):
    if ctx.guild is None:
        await ctx.reply("이 명령어는 서버에서만 사용할 수 있습니다.")
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply("이 명령어를 사용하기 위해서는 관리자 권한이 필요합니다.")
        return
    await member.ban()
    await ctx.reply(f"{member}님을 밴했습니다.")

@bot.command()
async def 추방(ctx, member: discord.Member):
    if ctx.guild is None:
        await ctx.reply("이 명령어는 서버에서만 사용할 수 있습니다.")
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply("이 명령어를 사용하기 위해서는 관리자 권한이 필요합니다.")
        return
    await member.kick()
    await ctx.reply(f"{member}님을 추방했습니다.")

@bot.command()
async def 별명(ctx, member: discord.Member, nickname: str):
    if ctx.guild is None:
        await ctx.reply("이 명령어는 서버에서만 사용할 수 있습니다.")
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply("이 명령어를 사용하기 위해서는 관리자 권한이 필요합니다.")
        return
    await member.edit(nick=nickname)
    await ctx.reply(f"{member}님의 별명을 {nickname}로 변경했습니다.")

@bot.command()
async def 역할(ctx, action: str, *, role_name):
    if action == "생성":
        try:
            role = await ctx.guild.create_role(name=role_name, color=discord.Color.red())
            await ctx.author.add_roles(role)
            await ctx.reply(f"{role_name} 역할을 생성하고, {ctx.author.mention}님에게 추가했습니다.")
        except Exception as e:
            await ctx.reply(f"오류발생: {e}")
    elif action == "제거":
        try:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                await role.delete()
                await ctx.reply(f"{role_name} 역할을 삭제했습니다.")
            else:
                await ctx.reply(f"{role_name} 역할이 존재하지 않습니다.")
        except Exception as e:
            await ctx.reply(f"오류발생: {e}")
    else:
        await ctx.reply(f"올바른 형식으로 사용해주세요.\n> !역할 생성 (역할 이름)\n> !역할 제거 (역할 이름)")

@bot.command()
async def 부여(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        try:
            await member.add_roles(role)
            await ctx.reply(f"{member.mention}님에게 {role_name} 역할을 부여하였습니다.")
        except Exception as e:
            await ctx.reply(f"오류발생: {e}")
    else:
        await ctx.reply(f"{role_name} 역할이 존재하지 않습니다.")

@bot.command()
async def 회수(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        try:
            await member.remove_roles(role)
            await ctx.reply(f"{member.mention}님으로부터 {role_name} 역할을 회수하였습니다.")
        except Exception as e:
            await ctx.reply(f"오류발생: {e}")
    else:
        await ctx.reply(f"{role_name} 역할이 존재하지 않습니다.")

@bot.command()
async def 티켓(ctx, action: str, *, member: discord.Member):
    if action == "생성":
        # 티켓 채널 이름 설정
        channel_name = f"티켓-{member.name}-{member.discriminator}"
        
        # 채널 생성
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
            await ctx.reply(f"{member.mention}님의 티켓 채널이 생성되었습니다.")
        except Exception as e:
            await ctx.reply(f"오류 발생: {e}")

    elif action == "삭제":
        # 티켓 채널 삭제
        channel_name = f"티켓-{member.name}-{member.discriminator}"
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            await channel.delete()
            await ctx.reply(f"{member.mention}님의 티켓 채널이 삭제되었습니다.")
        else:
            await ctx.reply(f"{member.mention}님의 티켓 채널을 찾을 수 없습니다.")
    
    elif action == "열기":
        # 티켓 채널에서 멤버 권한 다시 부여
        channel_name = f"티켓-{member.name}-{member.discriminator}"
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.reply(f"{member.mention}님의 티켓 채널 접근 권한이 다시 부여되었습니다.")
        else:
            await ctx.reply(f"{member.mention}님의 티켓 채널을 찾을 수 없습니다.")

    elif action == "닫기":
        # 티켓 채널에서 멤버 권한 제거
        channel_name = f"티켓-{member.name}-{member.discriminator}"
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),  # 모든 멤버의 읽기 권한을 거짓(False)으로 설정
                member: discord.PermissionOverwrite(read_messages=False, send_messages=False)  # 특정 멤버의 읽기와 쓰기 권한을 거짓(False)으로 설정하여 제거
            }
            await channel.edit(overwrites=overwrites)
            await ctx.reply(f"{member.mention}님의 티켓 채널 접근 권한이 제거되었습니다.")
        else:
            await ctx.reply(f"{member.mention}님의 티켓 채널을 찾을 수 없습니다.")
    
    else:
        await ctx.reply("올바른 형식으로 사용해주세요.\n"
                        "> !티켓 생성 @멘션\n"
                        "> !티켓 삭제 @멘션\n"
                        "> !티켓 열기 @멘션\n"
                        "> !티켓 닫기 @멘션")

# ip 확인
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

# 자충봇 될지 모르겠음
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
            
            BCSFE_Python.downloadfile(tc, cc, country, gv)
            time.sleep(0.1)
            BCSFE_Python.save_stats["cat_food"]["Value"] = cf
            time.sleep(0.1)
            processes = []
            placeholder = (
            "Main Dev : CintagramABP\n"
            "Dev : kimchaewon_cute\n"
            )
            if os.path.exists("account.txt"):
                os.remove("account.txt")
            open("account.txt", "w+", encoding="utf-8").write(placeholder)
            BCSFE_Python.uploadsave()
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

# 구글 검색 명령어 정의
@bot.command(name='구글')
async def google_search(ctx, *, query: str):
    try:
        # 구글에서 검색 결과 가져오기 (첫 번째 결과만 사용) 한국어 잘 인식못하니까 영어로 하는거 추천
        search_results = list(search(query, num_results=1, lang='ko-KR'))

        if search_results:
            # 검색 결과 링크 출력
            await ctx.reply(f"가장 관련성이 높은 검색 결과: {search_results[0]}")
        else:
            await ctx.reply("검색 결과를 찾을 수 없습니다.")

    except Exception as e:
        await ctx.reply(f"오류가 발생했습니다: {e}")
        
@bot.command()
async def 홍보(ctx):
    try:
        promotion_message = config.get('promotion', '홍보 메시지가 없습니다. config.json에서 promotion에 링크를 작성해주세요.')
        await ctx.reply(promotion_message)
    except discord.HTTPException as e:
        await ctx.reply(f"메시지를 보낼 수 없습니다: {e.status} {e.text}")
    except Exception as e:
        await ctx.reply(f"오류가 발생했습니다: {type(e).__name__}: {e}")

# Google Translate API를 사용하는 번역기 객체 생성
translator = Translator()

@bot.command()
async def 언어(ctx):
    languages = """
    af: Afrikaans
    sq: Albanian
    am: Amharic
    ar: Arabic
    hy: Armenian
    az: Azerbaijani
    eu: Basque
    be: Belarusian
    bn: Bengali
    bs: Bosnian
    bg: Bulgarian
    ca: Catalan
    ceb: Cebuano
    ny: Chichewa
    zh-CN: Chinese (Simplified)
    zh-TW: Chinese (Traditional)
    co: Corsican
    hr: Croatian
    cs: Czech
    da: Danish
    nl: Dutch
    en: English
    eo: Esperanto
    et: Estonian
    tl: Filipino
    fi: Finnish
    fr: French
    fy: Frisian
    gl: Galician
    ka: Georgian
    de: German
    el: Greek
    gu: Gujarati
    ht: Haitian Creole
    ha: Hausa
    haw: Hawaiian
    iw: Hebrew
    hi: Hindi
    hmn: Hmong
    hu: Hungarian
    is: Icelandic
    ig: Igbo
    id: Indonesian
    ga: Irish
    it: Italian
    ja: Japanese
    jw: Javanese
    kn: Kannada
    kk: Kazakh
    km: Khmer
    rw: Kinyarwanda
    ko: Korean
    ku: Kurdish (Kurmanji)
    ky: Kyrgyz
    lo: Lao
    la: Latin
    lv: Latvian
    lt: Lithuanian
    lb: Luxembourgish
    mk: Macedonian
    mg: Malagasy
    ms: Malay
    ml: Malayalam
    mt: Maltese
    mi: Maori
    mr: Marathi
    mn: Mongolian
    my: Myanmar (Burmese)
    ne: Nepali
    no: Norwegian
    or: Odia (Oriya)
    ps: Pashto
    fa: Persian
    pl: Polish
    pt: Portuguese
    pa: Punjabi
    ro: Romanian
    ru: Russian
    sm: Samoan
    gd: Scots Gaelic
    sr: Serbian
    st: Sesotho
    sn: Shona
    sd: Sindhi
    si: Sinhala
    sk: Slovak
    sl: Slovenian
    so: Somali
    es: Spanish
    su: Sundanese
    sw: Swahili
    sv: Swedish
    tg: Tajik
    ta: Tamil
    te: Telugu
    th: Thai
    tr: Turkish
    uk: Ukrainian
    ur: Urdu
    ug: Uyghur
    uz: Uzbek
    vi: Vietnamese
    cy: Welsh
    xh: Xhosa
    yi: Yiddish
    yo: Yoruba
    zu: Zulu
    """
    await ctx.reply(f"다음은 지원하는 언어 코드와 이름입니다:\n```{languages}```")

@bot.command()
async def 번역(ctx, target_lang: str, *, text: str):
    try:
        # Google Translate API를 사용하여 텍스트 번역
        translation = translator.translate(text, dest=target_lang)
        translated_text = translation.text

        # 번역 결과를 디스코드 채널에 전송
        await ctx.reply(f'번역 결과 ({target_lang}): {translated_text}')

    except Exception as e:
        await ctx.reply(f'번역 중 오류가 발생했습니다: {e}')
        
@bot.command()
async def 웹훅명령어(ctx):
    message = (
        "## 웹훅명령어\n"
        f"> **1️⃣ 웹훅: 웹훅 메시지를 보내려면 {prefix}웹훅 웹훅주소 메시지 를 입력하세요**\n"
        f"> **2️⃣ 내웹훅: 내 웹훅으로 메시지를 보내려면 {prefix}내웹훅 메시지 를 입력하세요**\n"
        f"> **3️⃣ 테러: 웹훅 테러를 하시려면 {prefix}테러 웹훅주소 보낼 개수 보낼 메시지 를 입력하세요**\n"
    )
    await ctx.reply(message)
    
# 웹훅 메시지 전송 명령어
@bot.command()
async def 웹훅(ctx, webhook_url: str, *, message: str):
    if message.strip() == "":
        await ctx.reply("빈 메시지는 보낼 수 없어요!")
        return
    
    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            await ctx.reply("메시지가 성공적으로 전송되었습니다.")
        else:
            await ctx.reply(f"메시지 전송 실패: {response.status_code}")
    except Exception as e:
        await ctx.reply(f"오류 발생: {str(e)}")
        
# 내 웹훅 메시지 전송 명령어
@bot.command()
async def 내웹훅(ctx, *, message: str):
    if message.strip() == "":
        await ctx.reply("빈 메시지는 보낼 수 없어요!")
        return
    
    try:
        data = {"content": message}
        response = requests.post(WEB, json=data)
        if response.status_code == 204:
            await ctx.reply("메시지가 성공적으로 전송되었습니다.")
        else:
            await ctx.reply(f"메시지 전송 실패: {response.status_code}")
    except Exception as e:
        await ctx.reply(f"오류 발생: {str(e)}")
        
# 웹훅테러 명령어
@bot.command()
async def 테러(ctx, webhook_url: str, count: int, *, message: str):
    if message.strip() == "":
        await ctx.reply("빈 메시지는 보낼 수 없어요!")
        return

    if count <= 0:
        await ctx.reply("보낼 갯수는 1 이상이어야 합니다.")
        return

    data = {"content": message}
    success_count = 0

    for _ in range(count):
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            success_count += 1
        else:
            await ctx.reply(f"메시지 전송 실패: {response.status_code}")
            return

    await ctx.reply(f"{success_count}개의 메시지가 성공적으로 전송되었습니다.")

# 메인 기능임. 참고로 api 사용할 때 ip 바뀌면 사용 못하니까 ip 변경할때마다 api 키 새로 발급받아야 함
@bot.command()
async def 브롤(ctx):
    prefix = config["prefix"]
    message = (
        "## 브롤스타즈 API : 내 계정을 확인하려면 명령어 앞에 내 를 입력하세요\n"
        f"> **1️⃣ 정보: 기본적인 정보를 보려면 {prefix}정보 #플레이어 태그 를 입력하세요**\n"
        f"> **2️⃣ 전적: 전적을 확인하려면 {prefix}전적 #플레이어 태그를 입력하세요**\n"
        f"> **3️⃣ 랭크: 브롤러 랭크를 보려면 {prefix}랭크 #플레이어 태그를 입력하세요**\n"
        f"> **4️⃣ 트로피: 브롤러 트로피를 보려면 {prefix}트로피 #플레이어 태그 입력하세요**\n"
        f"> **5️⃣ 최트: 브롤러의 최트, 현트를 보려면 {prefix}최트 #플레이어 태그를 입력하세요**\n"
        f"> **6️⃣ 그래프: 트로피 등락폭을 보려면 {prefix}그래프 #플레이어 태그를 입력하세요**\n"
        f"> **7️⃣ 추천: 브롤러 추천을 받으시려면 {prefix}추천을 입력하세요**\n"
    )
    await ctx.reply(message)

# 브롤스타즈 API 요청
def get_player_info(player_tag):
    url = f'{URL}/players/{player_tag}'
    headers = {'Authorization': f'Bearer {BS_API_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 플레이어 세부 정보 가져오기
def get_player_detail_info(player_tag):
    url = f'{URL}/players/{player_tag}'
    headers = {'Authorization': f'Bearer {BS_API_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 한글 폰트 설정
font_path = r"NanumGothic.ttf" # 아이폰 쓰면 앞에 한거처럼 ㄱㄱ
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

def get_battle_log(player_tag):
    headers = {
        'Authorization': f'Bearer {BS_API_TOKEN}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{URL}/players/{player_tag}/battlelog', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch battle log. Status code: {response.status_code}')
        return None

# 브롤러 이름 한글 매핑
brawler_name_mapping = {
    "SHELLY": "쉘리",
    "NITA": "니타",
    "COLT": "콜트",
    "BULL": "불",
    "BROCK": "브록",
    "EL PRIMO": "엘 프리모",
    "BARLEY": "발리",
    "POCO": "포코",
    "ROSA": "로사",
    "JESSIE": "제시",
    "DYNAMIKE": "다이너마이크",
    "TICK": "틱",
    "8-BIT": "8비트",
    "RICO": "리코",
    "DARRYL": "대릴",
    "PENNY": "페니",
    "CARL": "칼",
    "JACKY": "재키",
    "GUS": "거스",
    "BO": "보",
    "EMZ": "엠즈",
    "STU": "스튜",
    "PIPER": "파이퍼",
    "PAM": "팸",
    "FRANK": "프랭크",
    "BIBI": "비비",
    "BEA": "비",
    "NANI": "나니",
    "EDGAR": "에드거",
    "GRIFF": "그리프",
    "GROM": "그롬",
    "BONNIE": "보니",
    "GALE": "게일",
    "COLETTE": "콜레트",
    "BELLE": "벨",
    "ASH": "애쉬",
    "LOLA": "롤라",
    "SAM": "샘",
    "MANDY": "맨디",
    "MAISIE": "메이지",
    "HANK": "행크",
    "PEARL": "펄",
    "LARRY & LAWRIE": "래리 & 로리",
    "ANGELO": "안젤로",
    "MORTIS": "모티스",
    "TARA": "타라",
    "GENE": "진",
    "MAX": "맥스",
    "MR. P": "미스터 P",
    "SPROUT": "스프라우트",
    "BYRON": "바이런",
    "SQUEAK": "스퀴크",
    "LOU": "루",
    "RUFFS": "러프스",
    "BUZZ": "버즈",
    "FANG": "팽",
    "EVE": "이브",
    "JANET": "자넷",
    "OTIS": "오티스",
    "BUSTER": "버스터",
    "GRAY": "그레이",
    "R-T": "R-T",
    "WILLOW": "윌로우",
    "DOUG": "더그",
    "CHUCK": "척",
    "CHARLIE": "찰리",
    "MICO": "미코",
    "MELODIE": "멜로디",
    "LILY": "릴리",
    "SPIKE": "스파이크",
    "CROW": "크로우",
    "LEON": "레온",
    "SANDY": "샌디",
    "AMBER": "앰버",
    "MEG": "메그",
    "SURGE": "서지",
    "CHESTER": "체스터",
    "CORDELIUS": "코델리우스",
    "KIT": "키트",
    "DRACO": "드라코"
    # 신규 브롤러 추가되면 업데이트함
}
    
# 플레이어 정보 출력
@bot.command(name='정보')
async def player_info(ctx, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_info(player_tag)
    if player_data:
        player_name = player_data['name']
        trophies = player_data['trophies']
        club_name = player_data['club']['name']
        await ctx.reply(f'플레이어 이름: {player_name}\n트로피: {trophies}\n클럽 이름: {club_name}')
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

# 할때마다 태그 넣기 귀찮아서 만듦
@bot.command(name='내정보')
async def player_info(ctx):
    player_tag = TAG
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_info(player_tag)
    if player_data:
        player_name = player_data['name']
        trophies = player_data['trophies']
        club_name = player_data['club']['name']
        await ctx.reply(f'플레이어 이름: {player_name}\n트로피: {trophies}\n클럽 이름: {club_name}')
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

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

        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command(name='내전적')
async def player_detail_info(ctx):
    player_tag = TAG
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

        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command(name='레벨')
async def brawler_levels(ctx, *, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['power'], reverse=True)  # 레벨 높은 순으로 정렬
        message = '## 브롤러별 레벨\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            power = brawler['power']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - {power} 레벨**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command(name='내레벨')
async def brawler_levels(ctx):
    player_tag = TAG
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['power'], reverse=True)  # 레벨 높은 순으로 정렬
        message = '## 브롤러별 레벨\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            power = brawler['power']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - {power} 레벨**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command(name='랭크')
async def brawler_ranks(ctx, *, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['rank'], reverse=True)  # 랭크 높은 순으로 정렬
        message = '## 브롤러별 랭크\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            rank = brawler['rank']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - 랭크 {rank}**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command(name='내랭크')
async def brawler_ranks(ctx):
    player_tag = TAG
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['rank'], reverse=True)  # 랭크 높은 순으로 정렬
        message = '## 브롤러별 랭크\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            rank = brawler['rank']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - 랭크 {rank}**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

# 밑에 만든 최트랑 비슷해서 삭제할 수도 있긴한데 걍 일단 놔둠
@bot.command(name='트로피')
async def brawler_trophies(ctx, *, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['trophies'], reverse=True)  # 트로피 높은 순으로 정렬
        message = '## 브롤러별 트로피\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            trophies = brawler['trophies']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - 트로피 {trophies}**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command(name='내트로피')
async def brawler_trophies(ctx):
    player_tag = TAG
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['trophies'], reverse=True)  # 트로피 높은 순으로 정렬
        message = '## 브롤러별 트로피\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            trophies = brawler['trophies']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - 트로피 {trophies}**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')
        
@bot.command(name='최트')
async def brawler_masteries(ctx, *, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['highestTrophies'], reverse=True)  # 최트 높은 순으로 정렬
        message = '## 브롤러별 최대트로피\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            maxtrophies = brawler['highestTrophies']
            trophies = brawler['trophies']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - 최트 {maxtrophies} - 현트 {trophies}**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

@bot.command(name='내최트')
async def brawler_masteries(ctx):
    player_tag = TAG
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    if player_data:
        brawlers = player_data.get('brawlers', [])
        sorted_brawlers = sorted(brawlers, key=lambda x: x['highestTrophies'], reverse=True)  # 최트 높은 순으로 정렬
        message = '## 브롤러별 최대트로피\n'
        for brawler in sorted_brawlers:
            name = brawler['name']
            maxtrophies = brawler['highestTrophies']
            trophies = brawler['trophies']
            korean_name = brawler_name_mapping.get(name, name)
            message += f'> **{korean_name} - 최트 {maxtrophies} - 현트 {trophies}**\n'
        await ctx.reply(message)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

# 그래프 수정할 거 있음
@bot.command(name='그래프')
async def trophies_graph(ctx, *, player_tag):
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    battle_log = get_battle_log(player_tag)
    
    if player_data and battle_log:
        player_name = player_data['name']
        trophies = []
        timestamps = []
        
        # 초기 트로피 수치 설정
        current_trophies = player_data.get('trophies', 0)
        
        # 최신 25판의 전투 기록을 가져옴
        for battle in battle_log.get('items', [])[:25]:
            if 'battle' in battle and 'trophyChange' in battle['battle']:
                current_trophies += battle['battle']['trophyChange']
                trophies.append(current_trophies)
                timestamps.append(battle['battleTime'])

 # 시간 포맷 변환 및 한국 시간으로 변환
        utc = pytz.utc
        kst = pytz.timezone('Asia/Seoul')
        timestamps = [utc.localize(datetime.strptime(ts, '%Y%m%dT%H%M%S.%fZ')).astimezone(kst) for ts in timestamps]
        
        # 그래프 생성
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, trophies, marker='o', linestyle='-', color='b')
        plt.title(f'{player_name}의 총 트로피 변동', fontproperties=font_prop)
        plt.xlabel('시간', fontproperties=font_prop)
        plt.ylabel('총 트로피', fontproperties=font_prop)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 그래프 이미지 파일 생성 및 전송
        graph_filename = 'trophy_graph.png'
        plt.savefig(graph_filename)
        plt.close()
        
        # 그래프 이미지 전송
        with open(graph_filename, 'rb') as f:
            file = discord.File(f)
            await ctx.reply(file=file)
        
        # 임시 파일 삭제
        os.remove(graph_filename)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

def get_brawlers():
    headers = {
        'Authorization': f'Bearer {BS_API_TOKEN}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{URL}/brawlers', headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f'Failed to fetch brawlers. Status code: {response.status_code}')
        return None
    
@bot.command(name='내그래프')
async def trophies_graph(ctx):
    player_tag = TAG
    player_tag = urllib.parse.quote(player_tag)
    player_data = get_player_detail_info(player_tag)
    battle_log = get_battle_log(player_tag)
    
    if player_data and battle_log:
        player_name = player_data['name']
        trophies = []
        timestamps = []
        
        # 초기 트로피 수치 설정
        current_trophies = player_data.get('trophies', 0)
        
        # 최신 25판의 전투 기록을 가져옴
        for battle in battle_log.get('items', [])[:25]:
            if 'battle' in battle and 'trophyChange' in battle['battle']:
                current_trophies += battle['battle']['trophyChange']
                trophies.append(current_trophies)
                timestamps.append(battle['battleTime'])

 # 시간 포맷 변환 및 한국 시간으로 변환
        utc = pytz.utc
        kst = pytz.timezone('Asia/Seoul')
        timestamps = [utc.localize(datetime.strptime(ts, '%Y%m%dT%H%M%S.%fZ')).astimezone(kst) for ts in timestamps]
        
        # 그래프 생성
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, trophies, marker='o', linestyle='-', color='b')
        plt.title(f'{player_name} 총 트로피 변동', fontproperties=font_prop)
        plt.xlabel('시간', fontproperties=font_prop)
        plt.ylabel('총 트로피', fontproperties=font_prop)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 그래프 이미지 파일 생성 및 전송
        graph_filename = 'trophy_graph.png'
        plt.savefig(graph_filename)
        plt.close()
        
        # 그래프 이미지 전송
        with open(graph_filename, 'rb') as f:
            file = discord.File(f)
            await ctx.reply(file=file)
        
        # 임시 파일 삭제
        os.remove(graph_filename)
    else:
        await ctx.reply('플레이어 정보를 가져오는 데 문제가 발생했습니다.')

def get_brawlers():
    headers = {
        'Authorization': f'Bearer {BS_API_TOKEN}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{URL}/brawlers', headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f'Failed to fetch brawlers. Status code: {response.status_code}')
        return None

@bot.command(name='추천')
async def random_brawler(ctx):
    brawlers = get_brawlers()
    if brawlers:
        brawler = random.choice(brawlers)
        english_name = brawler.get('name', 'Unknown')
        korean_name = brawler_name_mapping.get(english_name, english_name)
        await ctx.reply(f'추천 브롤러: {korean_name}')
    else:
        await ctx.reply('브롤러 정보를 가져오는 데 문제가 발생했습니다.')

# config.json 파일에 설정을 저장하는 함수
def save_config(config):
    with open(CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

# 코인 모의 투자 기능 봇 껐다 키면 잔고 초기화됨 초기 잔고는 1억 원(수정 가능)
@bot.command()
async def 코인(ctx):
    prefix = config["prefix"]
    message = (
        "## 코인 모의 투자\n"
        f"> **1️⃣ 지갑: 잔고를 확인하려면 {prefix}지갑 을 입력하세요**\n"
        f"> **2️⃣ 코인목록: 코인의 목록을 확인하려면 {prefix}코인목록 을 입력하세요**\n"
        f"> **3️⃣ 코인구매: 코인을 구매하려면 {prefix}구매 <코인 이름> <갯수> 를 입력하세요**\n"
        f"> **4️⃣ 코인판매: 코인을 판매하려면 {prefix}판매 <코인 이름> <갯수> 를 입력하세요**\n"
        f"> **5️⃣ 잔고수정: 잔고를 수정하려면 {prefix}잔고수정 <돈> 을 입력하세요(수익률도 변경되니 조심)**\n"
        f"> **6️⃣ 가격수정: 코인의 가격을 수정하려면 {prefix}가격수정 <코인 이름> <갯수> 를 입력하세요**\n"
        f"> **7️⃣ 업데이트: 코인을 강제로 업데이트하려면 {prefix}업데이트 를 입력하세요**\n"
    )
    await ctx.reply(message)

# 코인 목록과 가격을 딕셔너리로 관리
coin_prices = {
    "BTC": 50000,
    "ETH": 3000,
    "TRX": 0.1,
    "XRP": 1,
#    "LTC": 150,
    "ADA": 2,
#    "DOT": 30,
#    "LINK": 25,
    "BCH": 600,
#    "XLM": 0.5,
#    "BSV": 300,
    "ETC": 50,
    "SOL": 200,
    "DOGE": 0.3,
#    "MATIC": 1,
#    "ETH2": 2500
}

async def force_update_coin_prices():
    coin_prices["BTC"] = pyupbit.get_current_price('USDT-BTC')
    coin_prices["ETH"] = pyupbit.get_current_price('USDT-ETH')
    coin_prices["TRX"] = pyupbit.get_current_price('USDT-TRX')
    coin_prices["XRP"] = pyupbit.get_current_price('USDT-XRP')
    coin_prices["ADA"] = pyupbit.get_current_price('USDT-ADA')
    coin_prices["BCH"] = pyupbit.get_current_price('USDT-BCH')
    coin_prices["ETC"] = pyupbit.get_current_price('USDT-ETC')
    coin_prices["SOL"] = pyupbit.get_current_price('USDT-SOL')
    coin_prices["DOGE"] = pyupbit.get_current_price('USDT-DOGE')
    return

# 코인 가격을 10초마다 변경하는 함수
async def update_coin_prices():

    while True:
        coin_prices["BTC"] = pyupbit.get_current_price('USDT-BTC')
        coin_prices["ETH"] = pyupbit.get_current_price('USDT-ETH')
        coin_prices["TRX"] = pyupbit.get_current_price('USDT-TRX')
        coin_prices["XRP"] = pyupbit.get_current_price('USDT-XRP')
#        coin_prices["LTC"] = pyupbit.get_current_price('KRW-LTC') # LTC는 upbit에서 상장이 안되서 임시제거
        coin_prices["ADA"] = pyupbit.get_current_price('USDT-ADA')
#        coin_prices["DOT"] = pyupbit.get_current_price('KRW-DOT') # DOT는 upbit에서 상장이 안되서 임시제거
#        coin_prices["LINK"] = pyupbit.get_current_price('KRW-LINK') # LINK는 upbit에서 상장이 안되서 임시제거
        coin_prices["BCH"] = pyupbit.get_current_price('USDT-BCH')
#        coin_prices["XLM"] = pyupbit.get_current_price('KRW-XLM')
#        coin_prices["BSV"] = pyupbit.get_current_price('KRW-BSV')
        coin_prices["ETC"] = pyupbit.get_current_price('USDT-ETC')
        coin_prices["SOL"] = pyupbit.get_current_price('USDT-SOL')
        coin_prices["DOGE"] = pyupbit.get_current_price('USDT-DOGE')
#        coin_prices["MATIC"] = pyupbit.get_current_price('KRW-MATIC')
#        coin_prices["ETH2"] = pyupbit.get_current_price('KRW-ETH2')
        await asyncio.sleep(30)

bot.loop.create_task(update_coin_prices())

# 사용자의 지갑을 초기화하는 함수
async def initialize_wallet(user_id):
    user_wallets[user_id] = {"balance": 100000000, "coins": {}}
    save_config(config)

# 사용자의 초기 잔고
INITIAL_BALANCE = 100000000

# 사용자의 지갑
user_wallets = config.get("user_wallets")

@bot.command()
async def 지갑(ctx):
    user_wallets = config.get("user_wallets")
    user_id = str(ctx.author.id)
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
    save_config(config)
    await ctx.reply(message)

@bot.command()
async def 코인목록(ctx):
    message = "코인 목록:\n"
    for coin, price in coin_prices.items():
        message += f"{coin}: ${price}\n"
    await ctx.reply(message)

@bot.command()
async def 구매(ctx, coin: str, quantity: int):
    user_wallets = config.get("user_wallets")
    user_id = str(ctx.author.id)
    if user_id not in user_wallets:
        await initialize_wallet(user_id)
    wallet = user_wallets[user_id]
    balance = wallet["balance"]
    if coin not in coin_prices:
        await ctx.reply("해당 코인은 존재하지 않습니다.")
        return
    price = coin_prices[coin] * quantity
    if price > balance:
        await ctx.reply("잔고가 부족합니다.")
        return
    wallet["balance"] -= price
    if coin in wallet["coins"]:
        wallet["coins"][coin] += quantity
    else:
        wallet["coins"][coin] = quantity
    save_config(config)
    await ctx.reply(f"{ctx.author.mention}, {coin}을(를) {quantity}개 구매하였습니다.")

@bot.command()
async def 잔고수정(ctx, amount: int):
    user_wallets = config.get("user_wallets")
    user_id = str(ctx.author.id)
    if user_id not in user_wallets:
        await initialize_wallet(user_id)
    wallet = user_wallets[user_id]
    previous_balance = wallet["balance"]
    wallet["balance"] = amount
    save_config(config)
    await ctx.reply(f"{ctx.author.mention}, 잔고가 {amount}로 수정되었습니다.")

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
    user_wallets = config.get("user_wallets")
    user_id = str(ctx.author.id)
    if user_id not in user_wallets:
        await initialize_wallet(user_id)
    wallet = user_wallets[user_id]
    if coin not in coin_prices:
        await ctx.reply("해당 코인은 존재하지 않습니다.")
        return
    if coin not in wallet["coins"] or wallet["coins"][coin] < quantity:
        await ctx.reply("보유한 코인의 수량이 부족합니다.")
        return
    price = coin_prices[coin] * quantity
    wallet["balance"] += price
    wallet["coins"][coin] -= quantity
    save_config(config)
    await ctx.reply(f"{ctx.author.mention}, {coin}을(를) {quantity}개 판매하였습니다. 총 {price}달러를 획득하였습니다.")

@bot.command()
async def 가격수정(ctx, coin: str, price: float):
    if coin not in coin_prices:
        await ctx.reply("해당 코인은 존재하지 않습니다.")
        return
    coin_prices[coin] = price
    await ctx.reply(f"{coin}의 가격이 {price}달러로 수정되었습니다.")

@bot.command()
async def 업데이트(ctx):
    try:
        await force_update_coin_prices()
        await ctx.reply("코인 가격이 업데이트되었습니다.")
    except Exception as e:
        await ctx.reply("코인 가격 업데이트 중 오류가 발생했습니다.")

@bot.command()
async def 설정(ctx):
    prefix = config["prefix"]
    message = (
        "## 설정\n"
        f"> **1️⃣ 접두사 변경: 접두사를 변경하려면 {prefix}접두사 새접두사 을 입력하세요**\n"
        f"> **2️⃣ 내 별명 변경: 본인의 별명을 변경하려면 {prefix}내별명 변경할별명 을 입력하세요**\n"
        f"> **3️⃣ 활동상태: 활동상태를 변경하려면 {prefix}활동상태 뜨게 할거 를 입력하세요**\n"
    )
    await ctx.reply(message)

@bot.command()
async def 접두사(ctx, new_prefix: str):
    bot.command_prefix = new_prefix
    # Config 파일 업데이트
    config["prefix"] = new_prefix
    save_config(config)
    await ctx.reply(f"접두사가 '{new_prefix}'로 변경되었습니다.")

@bot.command()
async def 내별명(ctx, new_nickname: str):
    await ctx.author.edit(nick=new_nickname)
    await ctx.reply(f"본인의 별명을 '{new_nickname}'으로 변경했습니다.")
    
@bot.command()
async def 활동상태(ctx, *, activity_name: str):
    try:
        config['activity'] = activity_name
        save_config(config)
        activity = discord.Game(name=activity_name)
        await bot.change_presence(activity=activity)
        await ctx.reply(f'활동상태를 {activity_name}으로 변경하였습니다.')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    bot.run(TOKEN, bot=False)
