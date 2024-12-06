import os
import pandas as pd
from AmzonSpider import AmazonSpider


theme = ['T-shirt'] # 主题列表

page = 1 # 一共抓取多少页, 请设置在 1-20 之间，Amazon官方仅提供20页商品

A = AmazonSpider()
A.open_browser()
A.enter_page('主页')
A.get_asin(theme, page)
