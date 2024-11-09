import smtplib
from email.mime.text import MIMEText
import logging

class EmailSender:
    def __init__(self, config):
        self.config = config

    def send_email(self, content, subject=None):
        """发送邮件"""
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = subject or self.config['subject']
            msg['From'] = self.config['sender']
            msg['To'] = self.config['receiver']

            server = smtplib.SMTP_SSL(self.config['smtp_server'], 465)
            server.login(self.config['sender'], self.config['password'])
            server.send_message(msg)
            server.quit()
            logging.info("邮件发送成功")
            return True
        except Exception as e:
            logging.error(f"邮件发送失败: {str(e)}")
            return False 