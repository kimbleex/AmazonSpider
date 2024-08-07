import os
import pandas as pd
from AmzonSpider import AmazonSpider
from CutWord import cut_word
from tqdm import tqdm

# 主题
theme = 'macbook case glitter'

# 储存路径
savepath = './data/{}/'.format(theme)
if not os.path.exists(savepath):
    os.makedirs(savepath)


a = AmazonSpider()
a.star_browser()

filename = './read/{}-asin.csv'.format(theme)
df_asin = pd.read_csv(filename)
df_asin['check'] = 0
df_asin2 = df_asin[df_asin['check']!=1]
asins = df_asin2['asin'].tolist()

for i in tqdm(range(len(asins)),ncols=80):
    a.enter_page('QA', asins[i])
    try:
        a.qa(theme, savepath, asins[i])
    except:
        pass
    df_asin.loc[df_asin['asin']==asins[i], 'check'] = 1
    df_asin.to_csv(filename, index=False)

a.browser.close()


cut_word(theme, 'QA',['asin','Q','A'], 'Q')
cut_word(theme, 'QA',['asin','Q','A'], 'A')
