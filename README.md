# search-engine
Flask bulids a simple search engine
利用python的爬虫技术，爬取王者荣耀的英雄列表信息，并保存到数据库中(先保存到了一个html文件中)
然后在利用flask搭建了一个简易版的网站，根据输入的关键字来进行对王者荣耀英雄信息的查询

技术点：
  爬虫：利用beautifulsoup技术来进行对html文档的操作，提取有用信息。
  flask：基础flask
  python链接mysql：用的pymysql进行链接


用到的python库：
  在主页下有个requirement.txt  里面写了所有用到的python库，你只需要 pip install -r requirement.txt即可把所有的用到的库安装完成
