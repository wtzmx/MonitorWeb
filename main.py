import json
import time
import logging
import importlib
import pkgutil
from pathlib import Path
import monitors
from utils.email_sender import EmailSender

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crawler.log'
)

class WebsiteMonitor:
    def __init__(self, config_path='config.json'):
        self.load_config(config_path)
        self.email_sender = EmailSender(self.config['email'])
        self.load_monitors()

    def load_config(self, config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logging.info("配置文件加载成功")
        except Exception as e:
            logging.error(f"加载配置文件失败: {str(e)}")
            raise

    def load_monitors(self):
        """加载所有监控器"""
        self.monitor_instances = []
        
        # 动态导入monitors包下的所有模块
        for monitor_config in self.config['monitors']:
            monitor_type = monitor_config['type']
            try:
                # 根据type动态导入对应的监控类
                module_name = f"{monitor_type}_monitor"
                module = importlib.import_module(f"monitors.{module_name}")
                class_name = f"{monitor_type.capitalize()}Monitor"
                monitor_class = getattr(module, class_name)
                
                # 创建监控实例
                monitor = monitor_class(monitor_config, self.config['headers'])
                self.monitor_instances.append(monitor)
                logging.info(f"成功加载监控器: {monitor_type}")
            except Exception as e:
                logging.error(f"加载监控器失败 ({monitor_type}): {str(e)}")

    def send_startup_notification(self):
        """发送启动通知"""
        content_parts = ["网站监控已启动！\n"]
        
        for monitor in self.monitor_instances:
            content_parts.append(f"\n监控网站：{monitor.name}")
            content_parts.append(f"网址：{monitor.url}")
            content_parts.append("\n当前最新内容：")
            content_parts.append(monitor.get_current_content())
            content_parts.append("-" * 50)
        
        content_parts.append(f"\n检查间隔：{self.config['settings']['check_interval']}秒")
        
        self.email_sender.send_email("\n".join(content_parts), "网站监控启动通知")

    def start_monitor(self):
        """开始监控"""
        logging.info("开始监控网站...")
        self.send_startup_notification()
        
        while True:
            try:
                for monitor in self.monitor_instances:
                    updates = monitor.check_update()
                    if updates:
                        for update in updates:
                            content = f"""
网站：{monitor.name}
发现内容更新！

标题：{update['title']}
发布日期：{update['date']}
链接：{update['link']}
                            """
                            self.email_sender.send_email(content)
                
                time.sleep(self.config['settings']['check_interval'])
            except KeyboardInterrupt:
                logging.info("监控已停止")
                break
            except Exception as e:
                logging.error(f"监控过程发生错误: {str(e)}")
                time.sleep(self.config['settings']['error_interval'])

def main():
    try:
        monitor = WebsiteMonitor()
        monitor.start_monitor()
    except Exception as e:
        logging.error(f"程序启动失败: {str(e)}")

if __name__ == '__main__':
    main() 