import re
import os
import time
import pickle
import pandas as pd
from selenium import webdriver

def name_distribution(name, male):
    
    url = 'https://randalolson.com/name-age-calculator/index.html?Gender={}&Name={}'.format(male, name)

    browser.get(url)
    browser.delete_all_cookies()
    with open('cookies.pkl', 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            browser.add_cookie(cookie)
    browser.refresh()   
    try:
        html = browser.page_source
    except Exception as error:
        if male=='F':
            male = 'M'
        else:
            male='F'
        url = 'https://randalolson.com/name-age-calculator/index.html?Gender={}&Name={}'.format(male, name)
        browser.get(url)
        browser.delete_all_cookies()
        with open('cookies.pkl', 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                browser.add_cookie(cookie)
        browser.refresh()
        html = browser.page_source
    
    txt = re.findall('was born around (.*?) old.', html)[0]
    media = re.findall('(.*?) and', txt)[0]
    age = re.findall('and ranges from (.*?) years', txt)[0].replace(' to ','~')

    return  media, age, male

def get_age(theme):
    # 获取计算机用户名
    # username = os.getlogin()
    options = webdriver.ChromeOptions()
    # 设置用户目录 保持浏览器设置信息
    # userPath = 'user-data-dir=C:/Users/{}/AppData/Local/Google/Chrome/User Data'.format(username)
    # options.add_argument(userPath)
    global browser
    browser = webdriver.Chrome(options=options)
    # 窗口最大化
    browser.maximize_window()

    filename = './read/{}-name.csv'.format(theme)
    savepath = './result/{}/用户年龄分布.csv'.format(theme)

    df = pd.read_csv(filename)
    df2 = df[df['check']!=1]
    names = df2['name'].tolist()
    males = df2['male'].tolist()
    
    for i in range(len(names)):
        time.sleep(2)
        name = names[i]
        male = males[i]
        result = name_distribution(name, male)
        media = result[0]
        age = result[1]
        male = result[2]
        data = [name, male, media, age]
        dataframe = pd.DataFrame([data])
        
        dataframe.to_csv(savepath, mode='a', header=False, index=False, encoding='utf-8-sig')
        df.loc[df['name']==name, 'check']=1
        df.to_csv(filename, index=False)


# 该步骤之前需要准备好XXX-name.csv文件,使用chatgpt标注性别
get_age(theme='macbook case glitter')

