import cx_Oracle
import os
from flask import Flask, render_template, abort, jsonify

app = Flask(__name__)

def dbconnect():
    try:
        dbconnection = cx_Oracle.connect(os.environ['DBUSER'], os.environ['DBPWD'], os.environ['DBSVC'], encoding="UTF-8")
    except cx_Oracle.DatabaseError as e:
        abort(501)
    return dbconnection

def get_dbinfo(dbconnection):
    dbcursor = dbconnection.cursor()
    dbcursor.execute(
        "select DBID, NAME, CREATED, LOG_MODE, OPEN_MODE, DATABASE_ROLE, PLATFORM_NAME, DB_UNIQUE_NAME, CDB from v$database")
    columns = (
        "DBID", "NAME", "CREATED", "LOG_MODE", "OPEN_MODE", "DATABASE_ROLE", "PLATFORM_NAME", "DB_UNIQUE_NAME", "CDB")
    values = dbcursor.fetchone()
    dbinfo = dict(zip(columns, values))
    dbcursor.execute("select sysdate from dual")
    today, = dbcursor.fetchone()
    dbinfo["SYSDATE"] = today
    dbcursor.execute("select MACHINE from v$session")
    client_host, = dbcursor.fetchone()
    dbinfo["CLIENT_HOST"] = client_host
    return dbinfo

@app.route('/')
def index():
    dbconnection = dbconnect()
    dbinfo = get_dbinfo(dbconnection)
    dbconnection.close()
    return render_template('index.html', dbinfo_dict = dbinfo)

@app.route('/api/v1', methods=['GET'])
def get_info():
    dbconnection = dbconnect()
    dbinfo = get_dbinfo(dbconnection)
    dbconnection.close()
    return jsonify(dbinfo)

@app.errorhandler(404)
def not_found(error):
    return "404 error: not found", 404

@app.errorhandler(501)
def db_connect(error):
    return "501 error: Cannot connect to the database", 501

if __name__ == '__main__':
    app.run(host='0.0.0.0')