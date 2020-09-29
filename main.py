import discord
from discord.ext import commands
import os

# Prefixes and such can be changed here
bot = commands.Bot(command_prefix = "!!!", case_insensitive=True, self_bot=True, status=discord.Status.invisible)

# For passing variables
bot.variables_first_run = True
bot.variables_last_link = ""
bot.variables_index = 0

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

print("bot is ready")

@bot.command()
async def reload(ctx, cog):
    bot.reload_extension(f"cogs.{cog}")
    await ctx.send("☑️")

with open('config/token') as f:
    TOKEN = f.readline()

bot.run(str(TOKEN), bot=False)