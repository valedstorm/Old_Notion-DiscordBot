from discord.ext import commands
from functionality.utils import * # 自定的工具包
from functionality.notion_api import * # Notion交互包

# 而外引入
import discord

class Add(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["a"]) # a為別名
    async def add(self, ctx, *args):

        # 讓用戶知道程序正在處理中
        await ctx.trigger_typing()
        
        # 如果指令格式錯誤，顯示提示
        if len(args) == 0:
            embed = discord.Embed(
                title="Please enter a valid query",
                description="You can search by title by typing `"
                + self.bot.command_prefix
                + "add <url>`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        
        # 獲取即將要添加的url
        url = args[0]
        # 基本檢查它是url格式
        if Utils.checkURL(url):
            # 資料庫中是否有相同連結
            if NotionAPI.isExistURL(url):
                # bot發送提醒訊息
                embed = discord.Embed(
                    title="Record already exists",
                    description="the URL is added",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                return
            
            # 指令沒問題，準備添加到資料庫
            else:
                # 取得用戶輸入的標簽
                tags = Utils.getTags(args)
                # 取得用戶名（貢獻者）
                contributor = "@" + str(ctx.author).split("#")[0]
                # 標題，若返回`None`，需要處理成字串，避免去調用方法
                title = Utils.getTitle(url)
                str_title = "無法取得標題" if title is None else title

                # 執行寫入動作，會返回{狀態碼}和{狀態文字}
                response_status_code, response_text = NotionAPI.addAllData(contributor, url, title, tags)

                # 判斷與組織bot的提醒消息
                if response_status_code == 200:
                    embed = discord.Embed(
                        title="Success added",
                        description="Data added successfully to Notion database!",
                        color=discord.Color.green(),
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(
                        title="Success added",
                        description=f"Failed to add data to Notion database. Reason: {response_text}",
                        color=discord.Color.red(),
                    )
                    await ctx.send(embed=embed)
        
        # 若是URL格式檢查沒通過，設置提醒消息
        else:
            embed = discord.Embed(
                title="URL Format Invalid",
                description="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Add(bot))