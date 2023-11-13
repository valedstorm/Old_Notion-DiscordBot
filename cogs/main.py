from discord.ext import commands

class MAIN(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("嗨，我是一個 Cog")

def setup(bot):
    bot.add_cog(MAIN(bot))