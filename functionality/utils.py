# 工具包，旨在放一些復用型的Func
import validators
import requests
from bs4 import BeautifulSoup

class Utils:

    # 檢查網址格式
    @staticmethod
    def checkURL(url):
        if validators.url(url):
            return True
        return False

    @staticmethod
    def getTitle(url):
        # 模擬正常瀏覽器的請求頭，可根據需要增添其他頭
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        # 發送GET請求，並在其中添加headers
        response = requests.get(url, headers=headers)

        # 檢查請求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # 找到標題標簽
            title_tag = soup.find('title')
            # 獲取標題内容
            title = title_tag.text

            # 判斷編碼如果不是utf-8，進行轉換
            if response.encoding != 'utf-8':
                title = title.encode(response.encoding).decode('utf-8')

            return title
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None
    
    # 解析文本，取得用戶輸入的標簽
    @staticmethod
    def getTags(args):
        tags_list = [] # 把字符串拆分轉list
        final_tags_list = [] # 去空白、去重、轉小寫后存入的list
        
        for arg in args[1:]:
            # 把送進來的字符串拆分並放到list中
            tag_list = arg.split(",")
            for tag in tag_list:
                # 清除前後空白、轉小寫
                tag = tag.strip().lower()
                # 去除重複的標簽
                if tag and tag not in tags_list:
                    final_tags_list.append(tag)
        
        # 判斷除白、除重過後有沒有標簽，沒有則添加默認
        if len(final_tags_list) == 0:
            final_tags_list.append('misc')

        return final_tags_list
