import os
import logging
import discord
from discord.ext import commands

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
        filename="/var/log/snakebot.log", level=logging.INFO)

class Snake:
    def __init__(self, bot):
        self.bot = bot

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
        description="Snake Bot")
bot.add_cog(Snake(bot))

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="snakED"))
    logging.info('on_ready,{},presence state set'.format(bot.user.name))

@bot.event
async def on_member_update(before,after):
    correct_role = False
    live_role_exists = False
    for role in after.roles:
        if role.name == "Twitch Subscriber":
            correct_role = True
        if role.name == "Live":
            live_role_exists = True
    if not correct_role:
        return
    if after.game is None:
        return
    live_role = None
    for role in after.server.roles:
        if role.name == "Live":
            live_role = role
    if after.game.type != 1:
        if live_role_exists:
            await client.remove_roles(after, live_role, )
            return
    if live_role_exists:
        return
    if live_role is not None:
        await client.add_roles(after, live_role, )


bot.run(str(os.environ['DISCORD_BOTKEY']))
