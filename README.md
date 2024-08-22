# 通过抓取产品的标题/五点描述/评论/QA问答生成用户画像报告

[**注意事项**]程序可能会因为网络不稳定报错停止运行，在234程序中均设置了中断以便于报错后按照上次位置继续运行程序

```python
# 如果中断需要继续跑程序，需要注释这一行代码
df_asin['check'] = 0
```

## 操作流程

data存储的是数据源文件,result存储的是分词,用户年龄分布文件,read是程序需要读取的文件

### 01获取ASIN.py(亚马逊每个商品对应的唯一ID)

需要输入的参数:  
>`theme` 关键字，即输入的词  
>`page`  需要抓取的页数，根据亚马逊官网的情况，最大为20

输出的结果储存在: `./read/主题-asin.csv` 用于以下程序使用

### 02获取标题+五点描述+分词.py

需要输入的参数:  
>`theme` 同上

输出的结果储存在: `./result/主题名称/title分词结果`和`./data/主题名称/主题-title.csv`

### 03获取评论+分词.py

需要输入的参数:  
>`theme` 同上

输出的结果储存在: `./result/主题名称/content分词结果`和`firstname分词结果`以及`./data/主题名称/主题-reviewscsv`

### 04获取QA+分词.py(商品的用户提问和回答)

需要输入的参数:  
>`theme` 同上

输出的结果存储在: `./result/主题名称/QA分词结果.csv`和`./data/主题名称/主题-QA.csv`

=========================================================
2024.08.15更新，亚马逊取消了QA页面，QA无法再进行抓取
=========================================================

### 05获取姓名年龄分布.py

需要输入的参数:  
>`theme` 同上

需要准备的文件: `./read/主题-name.csv`, 该文件需要从firtname分词(03获取评论+分词.py运行结果)中选出100个姓名并且标注好性别，可以使用chatGPT来执行,将csv中前150行复制到GPT中让它返回CSV即可

输出的结果存储在: `./result/主题名称/用户画像分布.csv`

### 06合并生成报告

需要输入的参数:  
>`theme` 同上

输出的结果存储在: `./主题名称-用户画像报告.csv`  
