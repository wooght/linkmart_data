# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :WebDriverMiddleWare.py
@Author     :wooght
@Date       :2024/6/25 17:18
@Content    :webdriver 配置
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import redis

class WebDriverMiddleWare(object):
    driver = None           # chrome driver
    options = Options()     # chrome options
    exception = None        # 报错标题
    e = None                # 报错内容
    headless = True         # 是否无头模式

    cookie_name = ''        # 对应的redis存放cookie的key
    cookies = {}            # cookie键值对
    pool = redis.ConnectionPool(host="192.168.101.101", port=6379, db=0, socket_connect_timeout=2, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    exception_url = []      # 错误url 当捕获异常后,将url append到exception_url, 如果存在次列表中,异常将返回None, 如果不存在,将返回request

    def set_options(self):
        if self.headless: self.options.add_argument('--headless')   # 无头模式
        self.options.add_argument('--disable-gpu')  # 禁止gpu加速
        self.options.add_argument('--window-size=1600, 900')        # 窗口大小
        self.options.add_argument('--disable-infobars')  # 禁止提示自动化运行
        self.options.add_argument('--hide-scrollbars')  # 隐藏滚动条
        self.options.add_argument("--lang=zh_CN.UTF-8")  # 编码
        self.options.add_argument("--no-sandbox")  # 禁止沙盒模式
        self.options.add_argument('--log-level=0')  # 设置日志级别   INFO:0,WARNING:1,LOG_ERROR:2,LOG_FATAL:3
        self.options.add_argument('--no-first-run')  # 禁止首次运行向导
        prefs = {
            'profile.default_content_settings.popups': 0,  # 禁止弹出下载窗口
            'download.default_directory': 'downfile',  # 下载目录
        }
        self.options.experimental_options['prefs'] = prefs
        # self.options.add_experimental_option('prefs', prefs)
        # self.options.add_experimental_option('detach', True)  # 保持打开状态
        # 以下两个方法 屏蔽浏览器页头:自动化测试控制
        self.options.add_experimental_option('useAutomationExtension', False)  # 停用开发者模式
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.driver = webdriver.Chrome(self.options)

    def set_cookies(self, cookies):
        """
        设置webdriver的新cookie
        :param cookies: dict {key:value, key:value,...}
        :return: None
        """
        for key, value in cookies.items():
            print(key, '|', value)
            self.driver.add_cookie({'name':key.strip(), 'value':value.strip() if isinstance(value, str) else ''})

    def get_cookies(self):
        """
        获取webdriver的cookies
        :return: [{domain:,expiry:,name:,value:,path:,httpOnly:,..},{},{}...]
        """
        cookies = self.driver.get_cookies()     # get_cookies('cookie name') 获取单个cookie的值
        return cookies

    def save_cookies(self, cookies):
        """
        保存cookie到redis
        :param cookies: webdriver get到的cookie格式:[{},{},...]
        :return:None
        """
        cookie_temp = {}
        for cookie in cookies:
            self.r.hset(self.cookie_name, key=cookie['name'], value=str(cookie['value']))
            cookie_temp[cookie['name']] = cookie['value']
        # 当前新cookie
        self.cookies = cookie_temp

    def delay(self, s):
        time.sleep(s)

    def get_url(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            self.e = e
            self.exception = type(e).__name__
            return False

    def close_driver(self):
        if self.driver:
            self.driver.close()     # 关闭当前handle
            self.driver.quit()      # 退出webdriver
