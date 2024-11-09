import requests
from bs4 import BeautifulSoup
import logging

def test_shandong_crawler():
    # 配置
    url = "http://hrss.shandong.gov.cn/channels/ch00238/"
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
        items = soup.find_all('li', class_='pagedContent')
        
        if not items:
            print("No items found")
            return
        
        print(f"\nFound {len(items)} items")
        print("\nFirst 5 items:")
        
        for item in items[:5]:
            try:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    link = a_tag.get('href')
                    date = item.find('span').get_text(strip=True)
                    
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
    print("Starting Shandong crawler test...")
    test_shandong_crawler() 