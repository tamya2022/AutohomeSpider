# @Time    : 2023/1/24 23:35
# @Author  : tamya2020
# @File    : car_home_login.py
# @Description : 汽车之家模拟登录
import pickle
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from selenium.webdriver.support.ui import WebDriverWait

from geetest_challenge import GeeTest3


class CarLogin(GeeTest3):
    def __init__(self, path_full_img=None, path_notch_img=None, debug=False):
        super().__init__(
            debug=debug,
            path_full_img=path_full_img,
            path_notch_img=path_notch_img,
        )
        self.username = "自己的账号"
        self.password = "自己的密码"
        self.login_url = "https://account.autohome.com.cn/"
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument("--start-maximized")
        # 使用开发者权限隐藏正受到自动测试软件的控制。
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 15)

    def __del__(self):
        self.browser.close()

    @staticmethod
    def random_delay(self):
        """
        随机等待延时
        :param self:
        :return:
        """
        return random.randint(0, 3)

    def save_cookie_dict_txt(self, ctx):
        cookies = ''
        cookies_list = ctx.get_cookies()
        for i in cookies_list:
            cookies += i['name'] + '=' + i['value'] + '; '
        with open('cookies.txt', 'w', encoding='utf-8') as f:
            f.write(cookies)

    def save_cookie_pkl(self, ctx):
        pickle.dump(ctx.get_cookies(), open("cookies.pkl", "wb"))

    def main(self):
        ctx = self.browser
        ctx.get(self.login_url)
        ctx.delete_all_cookies()  # 先清除无效cookie

        while True:
            WebDriverWait(ctx, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='密码登录']"))
            ).click()
            time.sleep(1)
            username_box = self.wait.until(EC.element_to_be_clickable((By.ID, 'UserName')))
            password_box = self.wait.until(EC.element_to_be_clickable((By.ID, 'PassWord')))
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'SubmitLogin')))
            check_box = self.wait.until(EC.element_to_be_clickable((By.ID, 'check_submitpassword')))
            username_box.send_keys(self.username)
            time.sleep(0.5)
            password_box.send_keys(self.password)
            time.sleep(1)
            check_box.click()
            time.sleep(0.1)
            WebDriverWait(ctx, 15, ignored_exceptions=StaleElementReferenceException).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='account-number-login']//div[@class='geetest_radar_tip']"))
            ).click()
            time.sleep(1)
            # 直接通过，则进行登录
            try:
                WebDriverWait(ctx, 5).until(
                    EC.text_to_be_present_in_element(
                        locator=(By.XPATH,
                                 "//div[@class='account-number-login']//span[@class='geetest_success_radar_tip_content']"),
                        text_="验证成功",
                    )
                )
                submit_btn.click()
                time.sleep(1)
                break
            except TimeoutException:
                resp = False

            if not resp:
                try:
                    # 不是滑动验证码，就进行刷新，重新登录
                    WebDriverWait(ctx, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "geetest_fullpage_click_box"))
                    )
                    # 进行滑动处理
                    resp_slide = self.run(ctx)
                    print("slide:", resp_slide)
                    if resp_slide:
                        submit_btn.click()
                        time.sleep(1)
                        break
                    else:
                        ctx.refresh()
                except TimeoutException:
                    # 进行页面刷新
                    print("页面超时刷新")
                    ctx.refresh()

        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'auto-header-logo')))
        print('登录成功，保存cookies')
        self.save_cookie_pkl(ctx)


if __name__ == '__main__':
    CarLogin().main()
