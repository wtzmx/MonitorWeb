import requests
from bs4 import BeautifulSoup
import logging

def test_hhu_crawler():
    # 配置
    url = "https://gs.hhu.edu.cn/17278/list.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # 发送请求
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        # 打印响应状态和内容长度
        print(f"Response status: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        print("\nTesting content extraction...")
        
        # 解析内容
        soup = BeautifulSoup(response.text, 'html.parser')
        news_container = soup.find('div', class_='col_news_list listcon')
        if not news_container:
            print("No news container found")
            return
            
        news_list = news_container.find('ul', class_='news_list list2')
        if not news_list:
            print("No news list found")
            return
            
        items = news_list.find_all('li', class_='news')
        
        if not items:
            print("No items found in news list")
            return
        
        print(f"\nFound {len(items)} items")
        print("\nFirst 5 items:")
        
        for item in items[:5]:
            try:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    if not title:
                        font_tag = a_tag.find('font')
                        if font_tag:
                            title = font_tag.get_text(strip=True)
                    # 添加域名前缀
                    link = 'https://gs.hhu.edu.cn' + a_tag.get('href', '')
                    date = item.find('span', class_='news_meta').get_text(strip=True)
                    
                    print("\nItem details:")
                    print(f"Title: {title}")
                    print(f"Date: {date}")
                    print(f"Link: {link}")
                else:
                    print(f"\nCouldn't find a tag in item: {item}")
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                print(f"Item HTML: {item}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Starting HHU crawler test...")
    test_hhu_crawler()