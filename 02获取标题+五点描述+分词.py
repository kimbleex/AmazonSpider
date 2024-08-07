import os
import pandas as pd
from AmzonSpider import AmazonSpider
from CutWord import cut_word
from tqdm import tqdm

# 主题
theme = 'macbook case glitter'

# 源数据储存路径
savepath1 = './data/{}/'.format(theme)
if not os.path.exists(savepath1):
    os.makedirs(savepath1)

# 结果储存路径
savepath2 = './result/{}/'.format(theme)
if not os.path.exists(savepath2):
    os.makedirs(savepath2)

a = AmazonSpider()
a.star_browser()

filename = './read/{}-asin.csv'.format(theme)
df_asin = pd.read_csv(filename)
df_asin['check'] = 0
df_asin2 = df_asin[df_asin['check']!=1]
asins = df_asin2['asin'].tolist()

for asin in tqdm(asins, ncols=80):
    a.enter_page('商品页', asin)
    a.title(theme, savepath1, asin)
    df_asin.loc[df_asin['asin']==asin, 'check'] = 1
    
    df_asin.to_csv(filename, index=False)

a.browser.close()

cut_word(theme, 'title',  ['asin','title','price','url', 'fivepoint'], 'title')
cut_word(theme, 'title',  ['asin','title','price','url', 'fivepoint'], 'fivepoint')
