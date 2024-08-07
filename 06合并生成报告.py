import pandas as pd
import os

def merge_files(theme):

    # 选取所需要的列 合并三份文件到一个excel中,
    filepath1 = './data/{}/'.format(theme)
    filename1 = filepath1 + '{}-QA.csv'.format(theme)
    filename2 = filepath1 + '{}-reviews.csv'.format(theme)
    filename3 = filepath1 + '{}-title.csv'.format(theme)

    filepath2 = './result/{}/'.format(theme)
    filename4 =  filepath2 + '用户年龄分布.csv'
    filename10 = filepath2 + 'firstname分词结果.csv'

    df1 = pd.read_csv(filename1, names=['asin', 'Q', 'A'])

    df2 = pd.read_csv(filename2, names=['用户名', '评分', '购买日期', '款式', '评论标题', '评论内容'])
    df3 = pd.read_csv(filename3, names=['asin', '标题', '价格', '图片地址', '五点描述'])
    df4 = pd.read_csv(filename4, names=['姓名','性别','中位数','年龄范围'])
    df10 = pd.read_csv(filename10, names=['word','times'])

    filename5 =  filepath2 + 'Q分词结果.csv'
    filename6 =  filepath2 + 'A分词结果.csv'
    filename7 =  filepath2 + 'title分词结果.csv'
    filename8 =  filepath2 + 'fivepoint分词结果.csv'
    filename9 =  filepath2 + 'content分词结果.csv'
    
    df5 = pd.read_csv(filename5)
    df6 = pd.read_csv(filename6)
    df7 = pd.read_csv(filename7)
    df8 = pd.read_csv(filename8)
    df9 = pd.read_csv(filename9)

    df5 = df5.rename(columns={'word': 'Q_word', 'times': 'Q_count'})
    df6 = df6.rename(columns={'word': 'A_word', 'times': 'A_count'})
    df7 = df7.rename(columns={'word': 'Title_word', 'times': 'Title_count'})
    df8 = df8.rename(columns={'word': 'Fivepoint_word', 'times': 'Fivepoint_count'})
    df9 = df9.rename(columns={'word': 'Reviews_word', 'times': 'Reviews_count'})
   
    cutword_df = pd.concat([df5, df6, df7, df8, df9],axis=1)  


    savename = './' + theme + '-用户画像报告.xlsx'
    
    with pd.ExcelWriter(savename) as writer:
        
        cutword_df.to_excel(writer, sheet_name='分词', index=False)

        df1.to_excel(writer, sheet_name='QA原始数据', index=False)
        df2.to_excel(writer, sheet_name='评论原始数据', index=False)
        df3.to_excel(writer, sheet_name='标题原始数据', index=False)
        df4.to_excel(writer, sheet_name='用户年龄分布', index=False)
        df10.to_excel(writer, sheet_name='姓名分词统计', index=False)

theme = 'iphone case gold'
merge_files(theme)