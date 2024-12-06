import os
import pandas as pd
from AmzonSpider import AmazonSpider
from CutWord import cut_word
from tqdm import tqdm

# 主题
theme = 'T-shirt'
asin_path = './sample/{}-asin.csv'.format(theme)

a = AmazonSpider()
a.open_browser()

df_asin = pd.read_csv(asin_path, names=["asin", "check"])
df_asin['check'] = 0 
asins = df_asin[df_asin['check']!=1]['asin'].tolist()

for asin in tqdm(asins, ncols=80):
    a.enter_page('商品页', asin)
    a.title(theme, asin)
    df_asin.loc[df_asin['asin']==asin, 'check'] = 1
    df_asin.to_csv(asin_path, index=False, header=False)
a.browser.close()

cut_word(theme, 'title',  ['asin','title','price','url'], 'title')
