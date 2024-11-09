import requests
from bs4 import BeautifulSoup
import logging
import re

def test_zhejiang_crawler():
    # 配置
    url = "https://rlsbt.zj.gov.cn/col/col1229743683/index.html"
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
        script = soup.find('script', text=re.compile(r'<recordset>'))
        
        if not script:
            print("No script tag found with recordset")
            return
            
        content = script.string
        soup_records = BeautifulSoup(content, 'html.parser')
        records = soup_records.find_all('record')
        
        if not records:
            print("No records found")
            return
        
        print(f"\nFound {len(records)} records")
        print("\nFirst 5 records:")
        
        for record in records[:5]:
            try:
                item_soup = BeautifulSoup(record.text, 'html.parser')
                a_tag = item_soup.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    link = a_tag.get('href')
                    date = item_soup.find('span', class_='bt_time').get_text(strip=True)
                    
                    print("\nRecord details:")
                    print(f"Title: {title}")
                    print(f"Date: {date}")
                    print(f"Link: {link}")
                else:
                    print(f"\nCouldn't find a tag in record")
            except Exception as e:
                print(f"Error processing record: {str(e)}")
                print(f"Record HTML: {record}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Starting Zhejiang crawler test...")
    test_zhejiang_crawler() 