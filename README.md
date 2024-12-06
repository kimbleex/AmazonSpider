# 亚马逊 用户/商品画像 爬虫

## **注意事项**

1. 程序可能会因为网络不稳定报错停止运行，在234程序中均设置了中断以便于报错后按照上次位置继续运行程序.
2. `./sample`和`./result`目录均为展示目录，可以自行更改.

## 操作流程

我的样例主题设置为`T-shirt`.

### 01.asin.py

`asin`是`Amazon`平台商品对应的唯一`ID`.

功能:

- 爬取指定主题的`asin`列表，并保存为csv文件.

需要的参数:  

- `theme` 主题列表，即在亚马逊平台上输入的关键词，例如`手机`，`电脑`，`电视`等，最好设置为英文.
- `page`  需要抓取的页数，根据亚马逊官网的情况，最大为20.
爬取结果可以参考`./sample/T-shirt-asin.csv`

### 02.title.py

功能:

- 可以爬取指定`asin`商品的标题`title`，价格`price`以及商品的主图的链接`image url`.
- 将爬取的商品标题进行分词、统计词频.

需要的参数:

- `theme` 单个主题，在完成步骤一之后，可以将步骤一中的单个主题传入.

结果参考: `./sample/T-shirt-title.csv`和`./result/T-shirt/title-cutwords.csv`

### 03.reviews.py

功能:

- 抓取指定商品的所有评论，包括用户的用户名``，评论内容，给商品的星级评分.
- 将评论内容进行分词、统计词频.
- 将用户名进行分词、统计词频.

需要输入的参数:  

- `theme` 单个主题，在完成步骤一和步骤二之后，可以将主题传入.

输出结果参考: `./sample/T-shirt-reviews.csv`和`./result/T-shirt/content-cutwords.csv`以及`./result/T-shirt/firstname-cutwords.csv`

### 04获取QA+分词.py [已废弃]

**2024.08.15更新，亚马逊取消了QA页面，QA无法再进行抓取**

### 05.name_age.py

先决条件: 需要准备好一个用户名文件，并放置在`./sample/`目录下。复制步骤三中的输出文件`./result/T-shirt/firstname-cutwords.csv`中的数据，如果太多可以复制大概150行左右 到`ChatGPT`，让它返回`csv`格式内容。

`ChatGPT`问答模板: "根据输入的内容，去除可能不是人名的行，并新增一列标记性别，男性为`M`，女性为`F`，输出csv文件。"

需要输入的参数:  

- `theme` 同上

### 06.report.py

需要输入的参数:  

- `theme` 同上
