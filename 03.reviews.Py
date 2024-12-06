import os
import pandas as pd
from tqdm import tqdm
from AmzonSpider import AmazonSpider
from CutWord import cut_word

# 主题
theme = 'T-shirt'
asin_path = './sample/{}-asin.csv'.format(theme)
reviews_path = './sample/{}-reviews.csv'.format(theme)

# 结果存储路径
cutwords_save_path = './result/{}/'.format(theme)
if not os.path.exists(cutwords_save_path):
    os.makedirs(cutwords_save_path)

# 抓取评论
a = AmazonSpider()
a.open_browser()

df_asin = pd.read_csv(asin_path, names=['asin', 'check'])
df_asin['check'] = 0 # 如果中途程序因为网络问题中断，请注释这一行以继续运行
asins = df_asin[df_asin['check']!=1]['asin'].tolist()

for i in tqdm(range(len(asins)),desc="评论爬取总进度", ncols=80):
    a.enter_page('评论区', asins[i])
    a.product_reviews(theme, asins[i])
    df_asin.loc[df_asin['asin']==asins[i], 'check'] = 1
    df_asin.to_csv(asin_path, index=False, header=False)
a.browser.close()

# 对用户名进行分词
def cut_name(username):
    firstname = username.split(' ')[0]
    return firstname

reviews = pd.read_csv(reviews_path, names=['username', 'star', 'buytime', 'color','title', 'content'])
reviews['username'] = reviews['username'].astype(str)
reviews['firstname'] = reviews['username'].apply(cut_name)
df_firstname = reviews['firstname'].value_counts(ascending=False)
df_firstname.to_csv(cutwords_save_path + 'firstname-cutwords.csv', header=None)

# 对评论内容进行分词
cut_word(theme, 'reviews',  ['username','star','buytime','color','title','content'], 'content')