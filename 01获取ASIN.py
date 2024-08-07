import os
import pandas as pd
from AmzonSpider import AmazonSpider

# 主题
theme = 'macbook case glitter'
# 一共抓取多少页
page = 20

A = AmazonSpider()
A.star_browser()
A.enter_page('主页')
A.get_asin(theme, page)

filename= './read/{}-asin.csv'.format(theme) 
print(filename)
df = pd.read_csv(filename, names=['asin', 'check'])
df.drop_duplicates(keep='first', inplace=True)
df.to_csv(filename, index=False)