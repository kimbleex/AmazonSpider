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

    def star_browser(self):
        # 获取计算机用户名
        username = os.getlogin()
        self.browser_path = 'C:/Users/{}/AppData/Local/Google/Chrome/User Data'.format(username)
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir={}'.format(self.browser_path))
        options.add_argument('lang=en-US')
        # 设置用户目录 保持浏览器设置信息
        self.browser = webdriver.Chrome(options=options)
        # 窗口最大化
        self.browser.maximize_window()
    
    def enter_page(self, url, asin=None):
        urls = {
            '主页': 'https://www.amazon.com/',
            '商品页': 'https://www.amazon.com/dp/{}'.format(asin),
            '评论区': 'https://www.amazon.com/product-reviews/{}'.format(asin),
            'QA':'https://www.amazon.com/ask/questions/asin/{}'.format(asin)
        }
        self.browser.get(urls[url])
        time.sleep(5)

    def get_asin(self, theme, page):
        self.wait = WebDriverWait(self.browser, 500)
        # 根据搜索词 抓取Asin
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))

        for _ in range(len(theme)):
            searchbox = self.browser.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
            searchbox.clear() 
            searchbox.send_keys(theme)
            searchbox.send_keys(Keys.ENTER)
            # 等待加载
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="departments"]')))
            time.sleep(2)
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
                filename = './read/' + theme + '-asin.csv'
                df.to_csv(filename, mode='a', index=False, header=False)
                try:
                    nextbutton = self.browser.find_element(By.XPATH,'.//a[text()="下一页"]')
                    self.browser.execute_script("arguments[0].scrollIntoView();", nextbutton)
                    nextbutton.click()
                except:
                    pass
                time.sleep(5)

    def qa(self, theme, savepath, asin):
        page = self.browser.find_elements(By.XPATH, '//*[@id="askPaginationBar"]/ul/li')
        page = page[-2].text
        page = int(page)

        filename = savepath + theme + '-QA.csv'

        for p in range(page):
            qas = self.browser.find_elements(By.XPATH, '//*[@id="a-page"]/div[1]/div[6]/div/div/div/div/div[2]')
            for qa in qas:
                q = qa.find_element(By.XPATH, 'div/div/div[2]/a/span').text
                try:
                    a = qa.find_element(By.XPATH, 'div[2]/div/div[2]/span').text
                except:
                    a = None
                data = [asin, q, a]
                df = pd.DataFrame([data])

                df.to_csv(filename, mode='a', index=False, header=False, encoding='utf-8-sig')
            
            time.sleep(2)
            self.browser.find_element(By.XPATH, './/a[text()="Next"]').click()
            time.sleep(3)

    def title(self, theme, savepath, asin):

        title = self.browser.find_element(By.XPATH, '//*[@id="productTitle"]').text                                
        # js_script= 'return document.querySelector("#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span.a-offscreen").textContent;'  
        #
        js_script= 'return document.querySelector("#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.aok-offscreen").textContent;'  
        ##corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.aok-offscreen

        # price = self.browser.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[2]').text
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
        fivepoint = ''
        for point in points:
            fivepoint = fivepoint + point.text + '\n' 
        
        filename = savepath + theme + '-title.csv'
        data = [asin, title, price, imgurl, fivepoint]
        df = pd.DataFrame([data])
        df.to_csv(filename, mode='a', index=False, header=False, encoding='utf-8-sig')
        
    def product_reviews(self, theme, savepath, asin):
        # 获取评论总数 计算翻页次数
        page_div = self.browser.find_element(By.XPATH, '//*[@id="filter-info-section"]/div').text
        # print(page_div)
        try:
            page = int(re.findall(', (.*?)带评论', page_div)[0].replace(',', ''))
        except:
            page = int(re.findall(', (.*?)带评论', page_div)[0].replace(',', ''))
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
                    data = [username, star, buytime, color , title, content]
                    dataframe = pd.DataFrame([data])
                    filename = '{}{}-reviews.csv'.format(savepath, theme)
                    dataframe.to_csv(filename, mode='a', index=False, header=False, encoding='utf-8-sig')
                except:
                    pass
            if p+1 < page:
                # 翻页
                self.browser.find_element(By.XPATH, './/a[text()="下一页"]').click()
                time.sleep(2)
            else:
                time.sleep(1)   


