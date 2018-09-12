
# coding: utf-8

# In[10]:


import requests
from bs4 import BeautifulSoup

#爬取王者荣耀官网的英雄信息
conn=requests.get("http://pvp.qq.com/web201605/herolist.shtml")
#设置编码为gbk
conn.encoding="gbk"
#利用beautifulsoup来进行对html文档的操作
bs=BeautifulSoup(conn.text);
#寻找制定class的div
lst=bs.find_all(name='div',attrs={"class":"herolist-box"})


# In[11]:


string=str(lst)
#去掉开始和结束的中括号
string=string[1:-1]
#将爬取过来的div拼上html头
wangzhe_text="<html><head><meta charset='UTF-8'></meta></head>{}<body></body></html>".format(string)
print(wangzhe_text)


# In[12]:


#将内容写入一个html文档
with open('wangzhe3.html','w') as fout:
    fout.write(wangzhe_text)
    fout.close()


# In[13]:


#利用beautifulsoup获取所有的超链接的href属性
page_content= None
with open('wangzhe3.html',encoding='gbk') as html_data:
    page_content= html_data.read()
    
wangzhe_soup = BeautifulSoup(page_content, 'lxml') 
for item in wangzhe_soup.findAll('a'):
    if 'href' in item.attrs and item['href'].endswith('shtml'):
        #拼上http://pvp.qq.com/web201605/ 因为爬取过来的数据不包含这个，无法访问
        item['href']="http://pvp.qq.com/web201605/"+item['href']
        print(item['href'])


# In[14]:


#获取所有的英雄链接
page_content= None
with open('wangzhe3.html',encoding='gbk') as html_data:
    page_content= html_data.read()
    
wangzhe_soup = BeautifulSoup(page_content, 'lxml')    

all_heros = ["http://pvp.qq.com/web201605/"+item['href'] 
             for item in wangzhe_soup.findAll('a')
             if 'href' in item.attrs and item['href'].endswith("shtml")]
all_heros = all_heros[0:len(all_heros)]


# In[15]:


#定义一个获取指定url的页面信息的function
def get_page(page_url,encode):
    """
    based on the url, get the page information
    """
    try:
        r = requests.get(page_url)    
        r.encoding=encode
        return r.text
    except Exception as inst:
        return None


# In[16]:


#定义一个给定url，给定页面信息的function，将信息封装成一个dict
def extract_information(page_url,page_content):
    page_soup = BeautifulSoup(page_content, 'lxml')
    page_info = {}
    page_title = image_url = page_text= ""
    for script in page_soup(["script", "style"]):
        script.extract()          
    try:
        image_url = page_soup.find('img')['src'].strip('/')
        if not image_url.startswith("http"):
            image_url = "http://"+image_url
        page_text = ','.join([text for text in page_soup.stripped_strings])
        page_title = page_soup.title.text.strip('\n')
    except:
        image_url = ""
    finally:
        page_info= {"url": page_url,"title": page_title, "image": image_url,"content":page_text}

    return page_info


# In[17]:


#将信息封装到一个list里
lst2=[]
for hero in all_heros:
    page=get_page(hero,'gbk')
    lst=[]
    lst.append(hero)
    lst.append(extract_information(hero,page))
    lst2.append(lst)
print(lst2)


# In[18]:


#最后，将内容写入数据库中
import pymysql
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='test',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
with connection.cursor() as cursor:
    for item in lst2:
        query_sql= 'INSERT INTO document_page (url,title,image,description,pagecontent) VALUES ("{}", "{}","{}","{}","{}");'.format(
            item[1]['url'],item[1]['title'],item[1]['image'].strip('/'),item[1]['content'][:140],item[1]['content'])
        connection.commit()
        sta=cursor.execute(query_sql)
connection.close()

