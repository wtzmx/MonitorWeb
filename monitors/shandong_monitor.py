from base_monitor import BaseMonitor
from bs4 import BeautifulSoup
import logging

class ShandongMonitor(BaseMonitor):
    def get_current_content(self):
        """获取当前网页内容"""
        try:
            response = self.make_request()
            if not response:
                return "获取内容失败"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('li', class_='pagedContent')
            
            content_list = []
            for item in items[:5]:  # 只获取最新的5条
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    link = self.get_full_url(a_tag.get('href'))
                    date = item.find('span').get_text(strip=True)
                    content_list.append(f"标题：{title}\n发布日期：{date}\n链接：{link}\n")
            
            return "\n".join(content_list)
            
        except Exception as e:
            logging.error(f"获取当前内容失败 ({self.name}): {str(e)}")
            return f"获取当前内容失败: {self.name}"

    def check_update(self):
        """检查网页更新"""
        try:
            response = self.make_request()
            if not response:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('li', class_='pagedContent')
            
            current_items = []
            for item in items:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    link = self.get_full_url(a_tag.get('href'))
                    date = item.find('span').get_text(strip=True)
                    current_items.append({
                        'title': title,
                        'link': link,
                        'date': date
                    })
            
            # 如果是第一次检查，保存当前内容并返回空
            if self.last_content is None:
                self.last_content = {item['title']: item for item in current_items}
                return []
            
            # 检查新内容
            updates = []
            for item in current_items:
                if item['title'] not in self.last_content:
                    updates.append(item)
            
            # 更新存储的内容
            self.last_content = {item['title']: item for item in current_items}
            
            return updates
            
        except Exception as e:
            logging.error(f"检查更新失败 ({self.name}): {str(e)}")
            return [] 