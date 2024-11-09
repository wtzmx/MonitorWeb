from base_monitor import BaseMonitor
from bs4 import BeautifulSoup
import logging

class HhuMonitor(BaseMonitor):
    def get_current_content(self):
        """获取当前网页内容"""
        try:
            response = self.make_request()
            if not response:
                return "获取内容失败"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_container = soup.find('div', class_='col_news_list listcon')
            if not news_container:
                return "未找到新闻容器"
            
            news_list = news_container.find('ul', class_='news_list list2')
            if not news_list:
                return "未找到新闻列表"
            
            items = news_list.find_all('li', class_='news')
            
            content_list = []
            for item in items[:5]:  # 只获取最新的5条
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    if not title:  # 如果title属性为空，尝试获取font标签内的文本
                        font_tag = a_tag.find('font')
                        if font_tag:
                            title = font_tag.get_text(strip=True)
                    # 添加域名前缀
                    link = 'https://gs.hhu.edu.cn' + a_tag.get('href', '')
                    date = item.find('span', class_='news_meta').get_text(strip=True)
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
            news_container = soup.find('div', class_='col_news_list listcon')
            if not news_container:
                return []
            
            news_list = news_container.find('ul', class_='news_list list2')
            if not news_list:
                return []
            
            items = news_list.find_all('li', class_='news')
            
            current_items = []
            for item in items:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag.get('title', '')
                    if not title:  # 如果title属性为空，尝试获取font标签内的文本
                        font_tag = a_tag.find('font')
                        if font_tag:
                            title = font_tag.get_text(strip=True)
                    # 添加域名前缀
                    link = 'https://gs.hhu.edu.cn' + a_tag.get('href', '')
                    date = item.find('span', class_='news_meta').get_text(strip=True)
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