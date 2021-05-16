from flask import Flask, Response, send_file, request, jsonify
import mysql.connector
import sys
import json
import socket
from glob import glob
import os

app = Flask(__name__)

@app.route('/userLogin', methods = ['GET', 'POST'])
def chat():
    msg_received = request.get_json()
    msg_subject = msg_received["subject"]

    if msg_subject == "register":
        return register(msg_received)
    elif msg_subject == "login":
        return login(msg_received)
    else:
        return "Invalid request."

def register(msg_received):
    id = msg_received["id"]
    name = msg_received["name"]
    pw = msg_received["pw"]

    select_query = "SELECT * FROM users where id = " + "'" + id + "'"
    db_cursor.execute(select_query)
    records = db_cursor.fetchall()
    if len(records) != 0:
        return "Another user used the username. Please chose another username."

    insert_query = "INSERT INTO users (id,name,pw) VALUES (%s,%s,MD5(%s))"
    insert_values = (id,name,pw)
    try:
        db_cursor.execute(insert_query, insert_values)
        chat_db.commit()
        sql="CREATE TABLE "+name+"(title VARCHAR(255) NOT NULL, content VARCHAR(255) NOT NULL, registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)default character set utf8 collate utf8_general_ci"
        db_cursor.execute(sql)
        chat_db.commit()
        return "success"
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

def login(msg_received):
    id= msg_received["id"]
    pw = msg_received["pw"]

    select_query = "SELECT name FROM users where id = " + "'" + id + "' and pw = " + "MD5('" + pw + "')"
    db_cursor.execute(select_query)
    records = db_cursor.fetchall()

    if len(records) == 0:
        return "failure"
        return "success"
try:
    chat_db = mysql.connector.connect(host="localhost", user="root", passwd="0000", database="user",charset='utf8')
except:
    sys.exit("Error connecting to the database. Please check your inputs.")
db_cursor = chat_db.cursor()

@app.route('/userlogin', methods=['POST'])
def userLogin():
    user = request.get_json()  # json 데이터를 받아옴
    print(user)
    return jsonify(user)  # 받아온 데이터를 다시 전송

@app.route("/", methods=['POST', 'GET'])
def t2s():
    text = request.get_json()
    print(text)
    return send_file('audio.wav')
@app.route('/ai', methods = ['GET', 'POST'])
def ai():
    msg_received = request.get_json()
    print(msg_received)
    msg = msg_received["msg"]
    path = msg_received["path"]
    arr=path.split('/')
    if "읽어" in msg :
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return "http://%s:%s/audio/%s"% (s.getsockname()[0], PORT,arr[2])
    elif "요약" in msg :
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return "http://%s:%s/audio/%s" % (s.getsockname()[0], PORT, arr[2])
    else:
        return "fail"

@app.route('/audio/<category>/<audionum>')
def streamwav(category,audionum):
    print(audionum)
    def generate(category,audionum):
        with open("news/%s/%s.wav" %(category,audionum), "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(audionum), mimetype="audio/x-wav")


@app.route('/insert/<username>', methods=['POST', 'GET'])

def insert(username):
    msg_received = request.get_json()
    title = msg_received["title"]
    content = msg_received["content"]
    insert_query = "INSERT INTO "+username+" (title,content) VALUES (%s,%s)"
    insert_values = (title, content)
    try:
        db_cursor.execute(insert_query, insert_values)
        chat_db.commit()
        return "success"
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

@app.route('/getdata/<username>', methods=['POST', 'GET'])

def getdata(username):

    insert_query = "SELECT * FROM user."+username
    try:
        db_cursor.execute(insert_query)
        result=db_cursor.fetchall()
        sum_result_string=""
        for i in result:
            title, content, date = i
            date= date.strftime('%Y-%m-%d %H:%M:%S')
            result_string="{{"+title+"//"+content+"//"+date+"}}"
            sum_result_string+=result_string
        return sum_result_string
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

if __name__ == '__main__':
    PORT = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        print('[*] Open http://%s:%s on your browser ' % (s.getsockname()[0], PORT))

    app.run(host='0.0.0.0', port=PORT)
