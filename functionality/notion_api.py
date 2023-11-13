# 這裏負責處理與NotionAPI接口、溝通的行爲
import json
import requests
# 爲了使用變量
from config import notion_token, database_id
# 增加時間
from datetime import datetime
import pytz

class NotionAPI:

    # 檢查要加入資料庫的url是否已存在
    @staticmethod
    def isExistURL(url):
        # 看不懂沒關係，是NotionAPI規定的交互格式
        # 要發送給哪一個Notion端點（不同行爲，在Notion的端口也不同）
        endpoint_url = "https://api.notion.com/v1/databases/" + database_id + "/query"
        # 物件轉成json
        json_data = json.dumps({"filter": {"property": "URL", "url": {"equals": url}}})
        # 標頭要指定（token、version、content-type）
        headers = {
            "Authorization": notion_token,
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json",
        }
        response = requests.post(endpoint_url, headers=headers, data=json_data)
        try:
            result = response.json()["results"]
        except:
            return False
        if len(result) == 0:
            return False
        return True
    
    # 寫入資料到資料庫中
    @staticmethod
    def addAllData(contributor, url, title, tags):
        # 先設定時區
        current_timezone = pytz.timezone('Asia/Taipei')
        
        # 包裝成數據包
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                # 貢獻者
                "Contributor": {
                    "title": [
                        {"text": {"content": contributor}}
                    ]
                },
                # 創建時間
                "Created_time": {
                    "date": {"start": datetime.now().astimezone(current_timezone).isoformat()}
                },
                # URL（名稱 - 類型 - 内容）
                "URL": {"url": url},
                # 標題（文字框的固定寫法）
                "Title": {
                    "rich_text": [
                        {
                            "text": {"content": title},
                            # 樣式添加，不是必須
                            "annotations": {
                                "bold": True,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "yellow"
                            }
                        }
                    ]
                },
                # 標簽
                "Tags": {
                    # 要經過包裝 {name: tag}
                    "multi_select": [
                        {"name": tag} for tag in tags
                    ]
                }
            }
        }

        # 設定標頭
        headers = {
            'Authorization': notion_token,
            'Notion-Version': '2021-05-13',
            'Content-Type': 'application/json'
        }

        # 數據包要發送到Notion的可接收的端點
        endpoint_url = "https://api.notion.com/v1/pages"

        # 這裏requests庫post，會把物件轉成JSON格式一次，所以在前面不能使用json.dumps()，會轉兩次造成格式錯誤
        response = requests.post(endpoint_url, headers=headers, json=data)

        # 返回 {狀態碼}還有{狀態文字}，交由呼叫者判斷、組織提示訊息
        return response.status_code, response.text