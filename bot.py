import os
import time
import logging
import discord

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

logging.basicConfig(
    format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
    filename="/var/log/snakebot.log",
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.WARNING)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="snakED"))
    log.info('on_ready,{0.user},presence state set'.format(client))

@client.event
async def on_member_update(before,after):
    await live_handler(after)

@client.event
async def on_message(m):
    if m.author == client.user:
        return
    if m.content == "F":
        if not lock_handler():
            return
        await m.channel.send("F")
        return
    if m.content == "^":
        if not lock_handler():
            return
        await m.channel.send("^")
        return
    if m.content.lower() == "beep":
        if not lock_handler():
            return
        await m.channel.send("BOOP")
        return
    if m.content.lower() == "!sync":
        await sync_handler(m)
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

async def sub_handler(m):
    if not lock_handler():
        return
    log.info("{} requested sub role".format(m.author.name))
    await m.channel.send(f"{m.author.mention} to receieve the Subscribers Role please link your twitch account to discord (Settings > Connections > Twitch Icon) and wait 30 minutes to an hour.")

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

async def sync_handler(m):
    user_count = 0
    for user in m.guild.members:
        user_count += 1
        await live_handler(user)
    await m.delete()
    log.info("sync_handler,synced {} users".format(user_count))

async def live_handler(after):
    live_role = after.guild.get_role(399778773265940481)
    live_role_exists = False
    for role in after.roles:
        if role == live_role:
            live_role_exists = True
            break
    live_streaming = False
    for act in after.activities:
        if act.type == discord.ActivityType.streaming:
            live_streaming = True
            break
    if not  live_streaming:
        if live_role_exists:
            await after.remove_roles(live_role, )
            log.info("live_handler,removing role from {}, not streaming"
                    .format(after.name))
        return
    sub_role = False
    for role in after.roles:
        if role.id == 398984088104730624:
            sub_role = True
    if not sub_role:
        return
    if live_role_exists:
        return
    if  live_streaming:
        await after.add_roles(live_role, )
        log.info("live_handler,adding role to {}".format(after.name))
        return

client.run(str(os.environ['DISCORD_BOTKEY']))
