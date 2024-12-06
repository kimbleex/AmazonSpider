import re
import os
import time
import math
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonSpider(object):
    def __init__(self):
        username = os.getlogin() # 获取当前用户名
        self.browser_path = 'C:/Users/{}/AppData/Local/Google/Chrome/User Data'.format(username) # 浏览器用户目录
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir={}'.format(self.browser_path)) # 设置用户目录 保持浏览器设置信息
        options.add_argument('lang=en-US') # 设置语言
        options.add_argument('ignore-certificate-errors') # 忽略证书错误
        options.add_argument("disable-blink-features=AutomationControlled") # 禁用浏览器被自动化控制
        options.add_argument("headless") # 设置无头模式
        options.add_argument("window-size=1920,1080") # 设置窗口大小
        # 设置用户目录 保持浏览器设置信息
        self.browser = webdriver.Chrome(options=options)
        # 窗口最大化
        self.browser.set_window_size(1920, 1080) # 设置窗口大小
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { 
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
            })
        self.wait = WebDriverWait(self.browser, 500) # 初始化等待时间
        self.save_path = "./sample/" # 保存asin的路径
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        
    def open_browser(self):
        self.browser.maximize_window()
    
    def enter_page(self, url, asin=None):
        urls = {
            '主页': 'https://www.amazon.com/',
            '商品页': 'https://www.amazon.com/dp/{}'.format(asin),
            '评论区': 'https://www.amazon.com/product-reviews/{}'.format(asin)
        }
        self.browser.get(urls[url])
        time.sleep(5)

    def get_asin(self, theme_list, page):
        # 根据搜索词 抓取Asin
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
        for i in range(len(theme_list)):
            searchbox = self.browser.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
            searchbox.clear() 
            searchbox.send_keys(theme_list[i])
            searchbox.send_keys(Keys.ENTER)
            # 等待加载
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="departments"]')))
            for _ in range(0, page):
                asins = self.browser.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div')
                results = []
                for a in asins:
                    try:
                        asin = a.get_attribute('data-asin')
                        results.append(asin)
                    except:
                        pass
                # 移除空白 
                while "" in results:
                    results.remove("")
                df = pd.Series(results)
                df.dropna(inplace=True)
                df.to_csv(self.asin_save_path + theme_list[i] + '-asin.csv', mode='a', index=False, header=False)
                try:
                    nextbutton = self.browser.find_element(By.XPATH,'.//a[text()="Next"]')
                    self.browser.execute_script("arguments[0].scrollIntoView();", nextbutton)
                    nextbutton.click()
                except:
                    pass
                time.sleep(5)
            asin_df = pd.read_csv(self.save_path + theme_list[i] + '-asin.csv')
            asin_df.drop_duplicates(keep='first', inplace=True)
            asin_df.to_csv(self.save_path + theme_list[i] + '-asin.csv', index=False, header=False)

    def title(self, theme, asin):

        title = self.browser.find_element(By.XPATH, '//*[@id="productTitle"]').text                                
        # js_script= 'return document.querySelector("#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span.a-offscreen").textContent;'  
        #
        js_script= 'return document.querySelector("#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.aok-offscreen").textContent;'  
        ##corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.aok-offscreen
        try:
            price = self.browser.execute_script(js_script)
            if 'with' in price:
                price = price.split('with')[0]
        except:
            price = None
        points = self.browser.find_elements(By.XPATH, '//*[@id="feature-bullets"]/ul/li/span')
        try:

            imgurl = self.browser.find_element(By.XPATH, '//*[@id="landingImage"]').get_attribute("src")
        except:
            imgurl = None
        
        filename = self.save_path + theme + '-title.csv'
        data = [asin, title, price, imgurl]
        df = pd.DataFrame([data])
        df.to_csv(filename, mode='a', index=False, header=False, encoding='utf-8-sig')
        
    def product_reviews(self, theme, asin):
        # 获取评论总数 计算翻页次数
        page_div = self.browser.find_element(By.XPATH, '//*[@id="filter-info-section"]/div').text
        try:
            page = int(re.findall(', (.*?) with reviews', page_div)[0].replace(',', ''))
        except:
            page = int(re.findall(', (.*?) with review', page_div)[0].replace(',', ''))
        page = 10 if int(math.ceil(page/10)) >= 10 else int(math.ceil(page/10))
        print("一共{}页".format(page))
        for p in tqdm(range(page), desc="当前asin:{}进度".format(asin),ncols=80):
            divs = self.browser.find_elements(By.XPATH, '//*[@id="cm_cr-review_list"]/div')
            for i in range(1,len(divs)-1):
                try:
                    self.browser.execute_script("arguments[0].scrollIntoView();", divs[i])
                    time.sleep(1)
                    username = divs[i].find_element(By.XPATH,'div/div/div[1]').text
                    star = divs[i].find_element(By.XPATH, 'div/div/div[2]/a/i/span').get_attribute("textContent").split('，')[0][0]
                    title = divs[i].find_element(By.XPATH, 'div/div/div[2]/a/span[2]').text
                    buytime = divs[i].find_element(By.XPATH, 'div/div/span').text.split(" ")[0]
                    try:
                        color = divs[i].find_element(By.XPATH, 'div/div/div[3]/a[1]').text.split(":")[1]
                    except:
                        color = " "
                    content = divs[i].find_element(By.XPATH, 'div/div/div[4]').text
                    dataframe = pd.DataFrame([[username, star, buytime, color , title, content]])
                    dataframe.to_csv(self.save_path + theme + '-reviews.csv', mode='a', index=False, header=False, encoding='utf-8-sig')
                except:
                    pass
            if p+1 < page:
                # 翻页
                self.browser.find_element(By.XPATH, './/a[text()="Next page"]').click()
                time.sleep(2)
            else:
                time.sleep(1)   


