# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :loginmiddlewares.py
@Author     :wooght
@Date       :2024/6/25 17:15
@Content    :实现美团收银的登录,cookie获取,保存,提取
"""
from app_spider.d_middlewares.WebDriverMiddleWare import WebDriverMiddleWare
from selenium.webdriver.common.by import By
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from scrapy.signals import spider_closed
from common.SecretCode import Wst
from common.w_re import CleanData
import time, json
from app_spider import models

class LoginMiddelWare(WebDriverMiddleWare):
    index_url = 'http://dpurl.cn/TAaQoHkz'                      # 判断登录成功地址

    clearn_data = CleanData('')
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 TitansX/11.11.15 KNB/1.0 iOS/17.4.1 App/(null)/1.18.8 meituangroup/com.meituan.erp.retail.admin/1.18.8 meituangroup/1.18.8 WKWebView'
    # 所需headers
    headers = {
        "openid": "",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Connection": "keep-alive",
        # "Host": "retailadmin-erp.meituan.com",
        "Origin": "https://retailadmin-erp.meituan.com",

        # Miscellaneous
        "posbrand": "MEITUAN",
        "poiid": 0,
        "appinfo": "retail-admin",
        "logintoken": '',
        "version": "v1.0",
        "platform": "3",
        "Referer": "",
        "sandbox": "",
        # 安全请求字段
        "Sec-Fetch-Mode": "cors",           # 请求模式  cors 跨域(response会有cors响应头),no-cors请求(response 无cors响应头)
                                            # no-cors 常用语图片,脚本,CSS等
                                            # same-origin 请求同源,不能跨域
                                            # navigate 页面切换,返回的内容应该是html
        "Sec-Fetch-Site": "same-origin",    # 发起者与目标之间的关系   cross-site 跨域请求, same-origin 同源, none 直接输入地址访问等
                                            # same-site 重定向相关
        "Sec-Fetch-Dest": "empty",          # 如何使用获取的数据/期望得到什么数据,document/frame/iframe/object/empty/font/image/worker/script
        # "Sec-Fetch-User": "?1"            # 用户是否激活触发 布尔值      ?1 请求由用户行为触发(点击导航,按钮等) ?0 由其他原因触发
        # "mtgsig":{"a1":"1.1", "a3":0}
    }

    def __init__(self):
        """
            获取爬虫运行所需数据:门店信息,账号信息,COOKIE列表
        """
        self.headless = True

        # 获取门店信息
        self.store_id = self.r.get('spider_store_id')
        mt_info = models.db.query(models.StoreList).filter_by(id=self.store_id).first()
        # 美团账号信息
        self.sy_user = mt_info.mt_user
        self.sy_password = Wst.decryption(mt_info.mt_password)
        self.sy_code = mt_info.mt_number

        # 获取上次成功登录的COOKIES
        self.cookie_name = 'meituan_' + str(self.store_id)
        self.cookies = self.r.hgetall(self.cookie_name)
        if len(self.cookies) < 1:
            self.set_option()

    @classmethod
    def from_crawler(cls, crawler):
        """
            注册中间件
        """
        s = cls()
        crawler.signals.connect(s.process_spider_closed, spider_closed)
        return s

    def set_option(self):
        """
            设置WebDriver并启动
        """
        self.options.add_argument("--user-agent={}".format(self.user_agent))  # user-agent
        super().set_options()
        if self.get_url(self.index_url):
            # 先打开网页才能设置cookie
            if len(self.cookies) > 0:
                self.set_cookies(self.cookies)
                self.delay(2)
                # self.driver.refresh()
                self.get_url(self.index_url)
                self.delay(2)
                if '商品' in self.driver.page_source:
                    print('cookie登录成功!')
                    self.close_driver()
                    return None
                else:
                    print('cookie 登录失败')
            print('尝试进入iframe进行登录')
            # 进入iframe
            src = self.driver.find_element(By.XPATH, '/html/body/section/iframe').get_attribute('src')
            self.delay(2)
            # self.driver.switch_to.frame(0)
            self.get_url(src)
            self.delay(2)
            self.driver.find_element(By.ID, 'part_key').send_keys(self.sy_code)
            self.driver.find_element(By.ID, 'login').send_keys(self.sy_user)
            self.driver.find_element(By.ID, 'password').send_keys(self.sy_password)
            self.delay(2)
            self.driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
            # self.driver.switch_to.parent_frame()
            self.delay(2)
            self.driver.save_screenshot('common/pic/shouyinresult.png')
            print('登录成功' if '商品' in self.driver.page_source else '登录失败')

            cookies = self.driver.get_cookies()
            self.save_cookies(cookies)
        else:
            raise IgnoreRequest('访问失败{}'.format(self.index_url))

    def process_request(self, request, spider):
        """
            请求包装
        """
        request.meta['store_id'] = self.store_id
        if 'native' in request.meta.keys():
            """ 
                scrapy 访问API
                组装headers,COOKIES
            """
            self.headers['poiid'] = self.cookies['retail-poiid']
            referer_model = "https://retailadmin-erp.meituan.com/report.html?bizlogintoken="
            self.headers['Referer'] = referer_model + self.cookies['erp-bsid'] + "&poiId=" + self.cookies[
                'retail-poiid'] + "&version=1.1.0&native_version=1.18.8&webview_launch={}&pos_brand=MEITUAN".format(str(int(time.time()*1000)))
            self.headers['logintoken'] = self.cookies['token-for-cors']
            for key, value in self.headers.items():
                request.headers[key] = value
            # request.headers.setdefault("User-Agent", self.user_agent)     # 无效果?
            request.headers['User-Agent'] = self.user_agent
            self.cookies['username'] = 'wooght'
            self.cookies['cityid'] = 0
            self.cookies['appId'] = 3
            self.cookies['login_token'] = self.cookies['token-for-cors']
            self.cookies['uuid'] = self.cookies['_lxsdk']
            self.cookies['_utm_content'] = self.cookies['uuid']
            self.cookies['retailadmin-app-native-version'] = '1.18.8'
            self.cookies['retailadmin-app-version'] = '1.1.0'
            request.cookies = self.cookies
            return None
        else:
            """ 
                WebDriver直接访问API
            """
            print('访问spider:{}提供的URL:{}'.format(spider.name, request.url))
            self.get_url(request.url)
            self.delay(1)
            self.set_cookies(self.cookies)
            self.delay(1)
            page = self.get_url(request.url)
            self.delay(1)
            if page:
                self.clearn_data.result_string = self.driver.page_source
                self.clearn_data.delete_html()
                return HtmlResponse(body=self.clearn_data.result_string, encoding='utf-8', request=request, url=request.url)
            else:
                raise IgnoreRequest('访问失败{}'.format(request.url))

    def process_response(self, request, response, spider):
        """
            响应数据判断
        """
        result_body = json.loads(response.body.decode('utf-8'))
        if 'error' in result_body.keys():
            print('process Response error :{}'.format(result_body))
            if request.url not in self.exception_url:
                self.exception_url.append(request.url)
                self.set_option()
                self.delay(6)
                return request
        return response

    def process_exception(self, request, exception, spider):
        """
            异常判断
        """
        print("捕获异常:{},url:{}".format(exception.__class__.__name__, request.url))
        """
            MaxRetryError
        """
        if request.url not in self.exception_url:
            self.exception_url.append(request.url)
            self.set_option()
        return None


    def process_spider_closed(self, spider, reason):
        self.close_driver()
