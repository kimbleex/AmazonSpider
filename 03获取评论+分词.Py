import os
import pandas as pd
from tqdm import tqdm
from AmzonSpider import AmazonSpider
from CutWord import cut_word

# 主题
theme = 'macbook case glitter'

# 数据存储路径
savepath1 = './data/{}/'.format(theme)
if not os.path.exists(savepath1):
    os.makedirs(savepath1)

# 结果存储路径
savepath2 = './result/{}/'.format(theme)
if not os.path.exists(savepath2):
    os.makedirs(savepath2)


# 抓取评论
a = AmazonSpider()
a.star_browser()

filename = './read/{}-asin.csv'.format(theme)
df_asin = pd.read_csv(filename)

# 重置check 如果报错想要按照之前的asin继续运行程序 请将此条代码注释
df_asin['check'] = 0

df_asin2 = df_asin[df_asin['check']!=1]
asins = df_asin2['asin'].tolist()

for i in tqdm(range(len(asins)),desc="评论爬取总进度", ncols=80):
    a.enter_page('评论区', asins[i])
    a.product_reviews(theme, savepath1, asins[i])
    df_asin.loc[df_asin['asin']==asins[i], 'check'] = 1
    df_asin.to_csv(filename, index=False)

a.browser.close()

# 合并评论
files = os.listdir(savepath1)
allData = pd.DataFrame()
for file in files:
    filepath = savepath1 + file
    df = pd.read_csv(filepath, names=['username', 'star', 'buytime', 'color','title', 'content'])
    df = df.drop_duplicates(keep='first')
    allData = pd.concat([allData, df])

allData['username'] = allData['username'].astype(str)

filename1 = './data/{}/{}-{}.csv'.format( theme,theme, 'reviews')
allData.to_csv(filename1, encoding='utf-8-sig', index=False, header=False)

# 对用户名进行分词
def cut_name(username):
    firstname = username.split(' ')[0]
    return firstname

reviews_filename = savepath1 + theme + '-reviews.csv'

allData = pd.read_csv(reviews_filename, names=['username', 'star', 'buytime', 'color','title', 'content'])
allData['username'] = allData['username'].astype(str)
allData['firstname'] = allData['username'].apply(cut_name)
df_firstname = allData['firstname'].value_counts(ascending=False)
filename2 = savepath2 + 'firstname分词结果.csv'
df_firstname.to_csv(filename2, header=None)

# 对评论内容进行分词
cut_word(theme, 'reviews',  ['username','star','buytime','color','title','content'], 'content')