# 用來連接.env檔與其他需要環境變量文件的中轉站，消除需要環境變量的文件之間發生循環依賴的問題
from dotenv import load_dotenv
import os

# 加载 .env 文件中的環境變量
load_dotenv()

# 读取环境变量的值
discord_token = os.getenv("DISCORD_TOKEN")
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")