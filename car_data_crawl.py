# @Time    : 2023/1/26 13:17
# @Author  : tamya2020
# @File    : car_data_crawl.py
# @Description :
import pickle
import time
import urllib.parse
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CarInfoCrawl:
    def __init__(self):
        self.index_url = "https://www.autohome.com.cn/zhoushan/"
        self.crawl_url = "https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-88.html"
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def hide_driver_info(self, ctx):
        # 1、加载该文件，用于隐藏特征
        with open('./stealth.min.js', encoding='utf-8') as f:
            js = f.read()

        ctx.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

    def add_cookie(self, ctx):
        # 2、加载cookie
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            ctx.add_cookie(cookie)
        ctx.refresh()

    def crawl_detail(self, ctx, detail_url_list):
        # 切换到新建标签页，进行遍历
        ctx.switch_to.window(ctx.window_handles[1])
        time.sleep(1)
        for url in detail_url_list[:3]:
            item = {}
            time.sleep(0.5)
            ctx.get(url)
            item['name'] = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="main-title"]/a'))).text
            item['price'] = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'font-arial'))).text
            print(item)
        print("*" * 28)

    def main(self):
        ctx = self.driver
        self.hide_driver_info(ctx)
        ctx.get(self.index_url)
        self.add_cookie(ctx)
        ctx.get(self.crawl_url)
        ctx.execute_script('window.open()')
        # 页面下拉，确保加载完成
        while True:
            # 滚动到底部
            ctx.execute_script("window.scrollTo(0,10000)")
            # 等待1秒
            time.sleep(1)
            # 3、获取详细请求链接
            detail_url_element_lists = ctx.find_elements(By.XPATH, "//div[@class='list-cont']/div/div[1]/a")
            detail_url_list = [urllib.parse.urljoin(self.crawl_url, element_url.get_attribute('href')) for element_url
                               in
                               detail_url_element_lists]
            # ctx.get("https://www.baidu.com")
            self.crawl_detail(ctx, detail_url_list)
            # 4、切换到列表页，进行翻页操作
            ctx.switch_to.window(ctx.window_handles[0])
            try:
                nextBtn = WebDriverWait(ctx, 10, ignored_exceptions=StaleElementReferenceException).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[text()='下一页']"))
                )
                # 判断是否末页
                next_url = nextBtn.get_attribute("href")
                if "java" in next_url:
                    break
                else:
                    nextBtn.click()
                time.sleep(1)
                # print(nextBtn.is_enabled())
            except TimeoutException:
                print("异常退出！")
                break


if __name__ == '__main__':
    CarInfoCrawl().main()
