from discord.ext import commands
import os
from config import discord_token # 爲了.env文件的變量

bot = commands.Bot(command_prefix='!')

# 起動完成時
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# 載入功能的指令
@bot.command(help="這是載入cogs内模組的命令")
async def load(ctx, extension):
    try:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Cog {extension} loaded.')
    except commands.ExtensionError as e:
        await ctx.send(f'Error loading {extension}: {e}')

# 卸載功能的指令
@bot.command(help="這是卸載cogs内模組的命令")
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Cog {extension} unloaded.')
    except commands.ExtensionError as e:
        await ctx.send(f'Error unloading {extension}: {e}')

# 重讀功能的指令
@bot.command(help="這是重載cogs内模組的命令")
async def reload(ctx, extension):
    try:
        bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'Cog {extension} reloaded.')
    except commands.ExtensionError as e:
        await ctx.send(f'Error reloading {extension}: {e}')

# 循環載入各部分指令模塊
# 在bot剛啟動時讀取所有檔案
for filename in os.listdir('./cogs'): # 移動到cogs的資料夾內
    if filename.endswith('.py'): # 找出所有結尾是.py的檔案
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(discord_token)