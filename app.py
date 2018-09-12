from flask import Flask, redirect,request
from flask import render_template
import pymysql

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

def connection_db(wd):
    connect=pymysql.Connect(
        host='localhost',
        user='root',
        passwd='root',
        db='test',
        charset='utf8'
    )
    cursor=connect.cursor()
    sql = "select * from document_page where pagecontent like '%{}%' limit 15".format(wd)
    cursor.execute(sql)
    lst = cursor.fetchall()
    return lst


@app.route("/search")
def search():
    wd = request.args.get('wd')
    lst = connection_db(wd)
    return render_template("searchResult.html", lst=lst)

if __name__ == '__main__':
    app.run()
