import os
import requests
import time
import asyncio
import logging
import discord

client = discord.Client()

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
        filename="/var/log/snakebot.log", level=logging.INFO)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="snakED"))
    logging.info('on_ready,{0.user},presence state set'.format(client))

@client.event
async def on_member_update(before,after):
    await live_handler(after)

@client.event
async def on_message(m):
    if m.author == client.user:
        return
    if m.content == "F":
        await f_handler(m)
        return
    if m.content == "^":
        await carot_handler(m)
        return
    if m.content.lower() == "beep":
        await beep_handler(m)
        return
    if "sub role" in m.content.lower():
        await sub_handler(m)
        return
    if "sub tag" in m.content.lower():
        await sub_handler(m)
        return
    if "!subrole" in m.content.lower():
        await sub_handler(m)
        return
    if m.content == "!sync":
        await sync_handler(m)
        return
    if m.content == "!activities":
        await m.channel.send(m.author.activities)
        return

async def sync_handler(m):
    for user in m.guild.members:
        await live_handler(user)

async def live_handler(after):
    live_role = after.guild.get_role(399778773265940481)
    live_role_exists = False
    for role in after.roles:
        if role == live_role:
            live_role_exists = True
            break
    if discord.Streaming not in after.activities:
        if live_role_exists:
            await after.remove_roles(live_role, )
            logging.info("removing role from {}, no game".format(after.name))
        return
    correct_role = False
    for role in after.roles:
        if role.id == "398984088104730624":
            correct_role = True
    if not correct_role:
        return
    if live_role_exists:
        return
    if discord.Streaming in after.activities:
        await after.add_roles(live_role, )
        logging.info("adding role from {}".format(after.name))
        return

async def sub_handler(m):
    if not lock_handler():
        return
    logging.info("{} requested sub role".format(m.author.name))
    await m.channel.send(m.author.mention+" to receieve the Subscribers Role please link your twitch account to discord (Settings > Connections > Twitch Icon) and wait 30 minutes to an hour.")

async def f_handler(m):
    if not lock_handler():
        return
    await m.channel.send("F")

async def carot_handler(m):
    if not lock_handler():
        return
    await m.channel.send("^")

async def beep_handler(m):
    if not lock_handler():
        return
    await m.channel.send("BOOP")

async def esports_background_task():
    await client.wait_until_ready()
    esportsChannel = client.get_channel("406591301790859274")
    while not client.is_closed:
        r = requests.get("https://api.twitch.tv/helix/streams?user_login=Rainbow6",
                headers={'Client-ID': str(os.environ['TWITCH_APIKEY'])})
        if r.json()["data"]:
            await esportsChannel.edit(name="esports",
                    topic="https://twitch.tv/Rainbow6")
            logging.info("Changing channel to #esports")
        else:
            await esportsChannel.edit(name="meta-discussion",
                    topic="Discussion around the meta of the game")
            logging.info("Changing channel to #meta-discussion")
        await asyncio.sleep(3600)

def lock_handler():
    lockFile = "/tmp/.kazlock"
    if os.path.isfile(lockFile):
        fileTime = os.path.getmtime(lockFile)
        if (time.time() - fileTime >= 120):
            os.remove(lockFile)
            f = open(lockFile, 'w+')
            f.close()
            return True
        return False
    f = open(lockFile, 'w+')
    f.close()
    return True

client.loop.create_task(esports_background_task())
client.run(str(os.environ['DISCORD_BOTKEY']))
