#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
exit = sys.exit

try:
    import config
except ImportError:
    print("config.py not found, copying one for you...")
    import shutil
    try:
        shutil.copyfile("config.example.py","config.py")
        print("Config file copied, follow the instructions inside to config the bot.")
    except FileNotFoundError:
        print("config.example.py not found, make sure you're in the script's directory!")
    exit(1)

import asyncio, json, random, requests
from telethon import TelegramClient, functions, types, events
from telethon.errors import *
from random import choice, sample
import logging

loop = asyncio.get_event_loop()

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s[%(name)s]: %(message)s")

log = logging.getLogger()

bot = TelegramClient('bot', config.api_id, config.api_hash).start(bot_token=config.bot_token)

client = bot

if config.logging != 0:
    async def log2chan(msg):
        await client.send_message(config.logging, msg)
else:
    async def log2chan(msg): pass

def escape(msg):
    return msg.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")

dresses_raw = requests.get("https://raw.githubusercontent.com/Borschts/EricDress/master/content.txt").text.split(",") + config.custom
dresses = []

str_listof_custom = "額外語錄列表：\n" + ",\n".join(config.custom)

zwnj = "‌"
for x in dresses_raw:
    dresses.append(x.replace("@ericliu1912","@" + zwnj + "ericliu1912"))

@client.on(events.InlineQuery)
async def handler(event):
    builder = event.builder

    msg = choice(sample(dresses,len(dresses)))
    emomsg = msg.replace("劉醬","EMO醬")
    emomsg = emomsg.replace("艾莉卡劉","惡魔寄")
    emomsg = emomsg.replace("ericaliu1912","EMOjiwiki")
    emomsg = emomsg.replace("劉華子","EMO醬")
    emomsg = emomsg.replace("艾力卡·劉","惡魔寄·EMO")
    emomsg = emomsg.replace("中華民國總統","總統") # 中華人民共和國總統！？？
    emomsg = emomsg.replace("中華民國","中華人民共和國")
    earthmsg = msg.replace("劉醬","地球醬")
    earthmsg = earthmsg.replace("艾莉卡劉","和平地球醬")
    earthmsg = earthmsg.replace("ericaliu1912","peacearth")
    earthmsg = earthmsg.replace("劉華子","地球醬")
    emomsg = emomsg.replace("艾力卡·劉","和平·地球醬")
    
    ans = [builder.article('劉醬快女裝！', text=msg),
        # builder.article('EMO醬快女裝！', text=emomsg),
        builder.article("地球醬快女裝！",text=earthmsg)
    ]
    if event.text.upper() == "EXTRALIST":
        ans.append(builder.article('額外語錄列表', text=str_listof_custom))

    await event.answer(ans)

    logmsg = "Inline query from `{}` given `{}`".format(escape(str(event._sender)),escape(msg))
    log.info(logmsg)
    await log2chan(logmsg)

@bot.on(events.NewMessage(pattern='/forcedress'))
async def cmd(event):
    msg = choice(sample(dresses,len(dresses)))

    await event.reply(msg,silent=True)

    logmsg = "CMD from `{}` given `{}`".format(escape(str(event.sender)),escape(msg))
    log.info(logmsg)
    await log2chan(logmsg)

bot.run_until_disconnected()
