from flask import Flask, redirect,request
from flask import render_template
import pymysql

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

def connection_db(wd,pageNow):
    connect=pymysql.Connect(
        host='localhost',
        user='root',
        passwd='root',
        db='test',
        charset='utf8'
    )
    cursor=connect.cursor()
    sql = "select * from document_page where pagecontent like '%{}%' limit {} , {}".format(wd, (pageNow-1)*5, 5 )
    cursor.execute(sql)
    lst = cursor.fetchall()
    return lst

def query_page_count(page_size):
    connect = pymysql.Connect(
        host='localhost',
        user='root',
        passwd='root',
        db='test',
        charset='utf8'
    )
    cursor = connect.cursor()
    sql = "select count(*) from document_page"
    cursor.execute(sql)
    all_count = cursor.fetchall()
    all_count = all_count[0][0]
    if all_count % page_size:
        return all_count // page_size + 1
    return all_count // page_size

@app.route("/search")
def search():
    wd = request.args.get('wd')
    pageNow = request.args.get('pageNow')
    pageNow = int(pageNow)
    print(pageNow)
    lst = connection_db(wd, pageNow)
    page_count = query_page_count(5)
    return render_template("searchResult.html", lst=lst, page_count=page_count)

if __name__ == '__main__':
    app.run()
