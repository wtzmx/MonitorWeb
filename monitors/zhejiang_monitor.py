from base_monitor import BaseMonitor
from bs4 import BeautifulSoup
import logging
import re

class ZhejiangMonitor(BaseMonitor):
    def get_current_content(self):
        """获取当前网页内容"""
        try:
            response = self.make_request()
            if not response:
                return "获取内容失败"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # 找到包含记录的script标签
            script = soup.find('script', text=re.compile(r'<recordset>'))
            if not script:
                return "未找到内容列表"
            
            # 从script内容中提取记录
            content = script.string
            soup_records = BeautifulSoup(content, 'html.parser')
            records = soup_records.find_all('record')
            
            content_list = []
            for record in records[:5]:  # 只获取最新的5条
                item_soup = BeautifulSoup(record.text, 'html.parser')
                a_tag = item_soup.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    link = self.get_full_url(a_tag.get('href'))
                    date = item_soup.find('span', class_='bt_time').get_text(strip=True)
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
            script = soup.find('script', text=re.compile(r'<recordset>'))
            if not script:
                return []
            
            content = script.string
            soup_records = BeautifulSoup(content, 'html.parser')
            records = soup_records.find_all('record')
            
            current_items = []
            for record in records:
                item_soup = BeautifulSoup(record.text, 'html.parser')
                a_tag = item_soup.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    link = self.get_full_url(a_tag.get('href'))
                    date = item_soup.find('span', class_='bt_time').get_text(strip=True)
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