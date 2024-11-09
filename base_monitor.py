from abc import ABC, abstractmethod
import logging
from bs4 import BeautifulSoup
import requests

class BaseMonitor(ABC):
    def __init__(self, config, headers):
        self.config = config
        self.headers = headers
        self.name = config['name']
        self.url = config['url']
        self.encoding = config['encoding']
        # 存储上一次检查的内容，用于比对更新
        self.last_content = None

    @abstractmethod
    def get_current_content(self):
        """获取当前网页内容"""
        pass

    @abstractmethod
    def check_update(self):
        """检查网页更新"""
        pass

    def make_request(self):
        """发送HTTP请求"""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.encoding = self.encoding
            return response
        except Exception as e:
            logging.error(f"请求失败 ({self.name}): {str(e)}")
            return None

    def get_full_url(self, href):
        """处理相对URL"""
        base_domain = '/'.join(self.url.split('/')[:3])
        
        if href.startswith('http'):
            return href
        elif href.startswith('..'):
            clean_path = href.replace('../', '')
            return f"{base_domain}/{clean_path}"
        elif href.startswith('/'):
            return f"{base_domain}{href}"
        else:
            return f"{base_domain}/{href}" 