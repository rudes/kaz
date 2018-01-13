import os
import logging
import discord

client = discord.Client()

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
        filename="/var/log/snakebot.log", level=logging.INFO)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="snakED"))
    logging.info('on_ready,{},presence state set'.format(client.user.name))

@client.event
async def on_member_update(before,after):
    live_role = None
    for role in after.server.roles:
        if role.name == "Live":
            live_role = role
            break
    if after.game is None:
        await client.remove_roles(after, live_role, )
        logging.info("removing role from {}, no game".format(after.name))
        return
    if after.game.type != 1:
        await client.remove_roles(after, live_role, )
        logging.info("removing role from {}, not streaming".format(after.name))
        return
    correct_role = False
    for role in after.roles:
        if role.name == "Twitch Subscriber":
            correct_role = True
    if not correct_role:
        return
    if after.game.type == 1:
        await client.add_roles(after, live_role, )
        logging.info("adding role from {}".format(after.name))
        return


client.run(str(os.environ['DISCORD_BOTKEY']))
