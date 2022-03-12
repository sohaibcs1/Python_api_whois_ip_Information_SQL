from decimal import MAX_PREC
from flask import Flask, redirect,flash, render_template,url_for,request,abort,json,send_from_directory
import urllib.request
from flask_mysqldb import MySQL
import yaml
import re
import whois
import os

app = Flask(__name__)


# Configure db
db = yaml.load(open('db.yaml'),Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

 
def ip_details(iip):
        ipcheck=0
        try:
            url="https://ipinfo.io/" + iip
            req=urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data=response.read()
                data=json.loads(data)
        except:
            ipcheck=1
            return ("Network-Problem/Not-Valid-Ip")
        if(ipcheck==0):
            try:
                my_dict = {"IP Address": data['ip'], "City:": data['city']
                , "State:": data['region']
                , "Country:": data['country']
                , "GPS:": data['loc']
                , "ZIP:": data['postal']
                , "ISP:": data['org']
                    }
                return (my_dict)
            except:
                my_dict2 = {"IP Address": "N/A", "City:": "N/A"
                , "State:": "N/A"
                , "Country:": "N/A"
                , "GPS:": "N/A"
                , "ZIP:": "N/A"
                , "ISP:": "N/A"
                    }
                return (my_dict2)


@app.route('/ip/<ip>',methods=['GET','POST'])
def ipcheck(ip): 
        ipdt=ip_details(ip)
        #db Start
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ip_details(ip,details) VALUES(%s, %s)",(ip, ipdt))
        mysql.connection.commit()
        cur.close()
        #db End
        return ipdt
        
@app.route('/whois/<who1>',methods=['GET','POST'])
def who(who1): 
    #res=whois.whois(who1)
    # #db Start
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO whois(ip_url,details) VALUES(%s, %s)",(who1, res))
    # mysql.connection.commit()
    # cur.close()
    # #db End
    #db Start
    cur = mysql.connection.cursor()
    cur.execute("select details from ip_details where ip LIKE %s",[who1])
    item = cur.fetchone()
    #db End
    print(item)
    return "r"


if __name__ =='__main__':
    app.run()
