import re
import os
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def cut_word(theme, fun, columns, column):

    filename = './data/{}/{}-{}.csv'.format(theme, theme, fun)
    data = pd.read_csv(filename,names=columns)
    data.drop_duplicates(keep='first', inplace=True)
    data[column] = data[column].astype(str)
    titles = data[column].to_list()

    stopWords = stopwords.words('english')

    allWords = []
    for title in titles:
        title = re.sub('\W+', ' ', title).replace("_", ' ')
        words = word_tokenize(title, 'english')
        for word in words:
            if word not in stopWords:
                if len(word)>1:
                    allWords.append(word)
    
    df = pd.Series(allWords)
    df = df.value_counts()
    df = df.to_frame().reset_index()
    
    savepath = './result/{}/'.format(theme)
    filename = './result/{}/{}分词结果.csv'.format(theme, column)
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    df.to_csv(filename, index=False, header=['word', 'times'], encoding='utf-8-sig')


