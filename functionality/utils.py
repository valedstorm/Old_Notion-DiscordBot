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
        try:
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            title_tag = soup.find("title")
            return title_tag.get_text()
        except:
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
