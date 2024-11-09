网站内容监控脚本

功能说明
本脚本用于监控指定网站的内容更新,当发现新内容时,会通过邮件发送通知。

目录结构
project/
├── config.json          # 配置文件
├── main.py             # 主程序
├── base_monitor.py     # 监控基类
├── monitors/           # 监控器目录
│   ├── __init__.py
│   ├── jiangnan_monitor.py  # 江南大学网站监控
│   ├── jshrss_monitor.py    # 江苏人社网站监控
│   ├── shu_monitor.py       # 上海大学网站监控
│   ├── hhu_monitor.py       # 河海大学网站监控
│   ├── muc_monitor.py       # 中央民族大学网站监控
│   ├── shandong_monitor.py  # 山东人社厅网站监控
│   └── zhejiang_monitor.py  # 浙江人社厅网站监控
├── utils/              # 工具目录
│   ├── __init__.py
│   └── email_sender.py # 邮件发送工具
└── tests/             # 测试目录
    ├── test_hhu.py    # 河海大学监控测试
    ├── test_shandong.py # 山东人社厅监控测试
    └── test_zhejiang.py # 浙江人社厅监控测试

使用说明

1. 环境要求
- Python 3.6+
- 依赖包:
  pip install requests
  pip install beautifulsoup4

2. 配置文件说明(config.json)
{
    "email": {
        "smtp_server": "邮件服务器地址",
        "sender": "发件人邮箱",
        "password": "邮箱授权码",
        "receiver": "收件人邮箱",
        "subject": "邮件主题"
    },
    "monitors": [
        {
            "name": "监控名称",
            "url": "监控网址",
            "encoding": "网页编码",
            "type": "监控器类型"
        }
    ],
    "settings": {
        "check_interval": 检查间隔(秒),
        "error_interval": 出错重试间隔(秒)
    }
}

3. 运行方法
python main.py

4. 添加新的网站监控
(1) 在monitors目录下创建新的监控类文件(example_monitor.py)
(2) 继承BaseMonitor类并实现必要的方法:
    - get_current_content(): 获取当前网页内容
    - check_update(): 检查网页更新
(3) 在config.json的monitors中添加对应配置

5. 日志说明
- 程序运行日志保存在crawler.log文件中
- 包含运行状态、错误信息等

6. 注意事项
- 确保config.json中的邮箱配置正确
- 邮箱密码使用授权码而非登���密码
- 检查间隔不要设置过短,建议至少1小时(3600秒)
- 添加新监控器时注意网页结构的解析

7. 错误处理
- 网络连接失败: 等待error_interval后重试
- 解析失败: 记录错误日志并继续监控
- 邮件发送失败: 记录错误日志但不中断监控

8. 支持的网站
- 江南大学研究生招生网
- 江苏人社网
- 上海大学研究生招生网
- 河海大学研究生院
- 中央民族大学研究生招生网
- 山东省事业单位招聘网
- 浙江省事业单位招聘网

9. 联系方式
如有问题请联系: your@email.com

版权说明
本脚本仅供学习交流使用,请勿用于商业用途。 