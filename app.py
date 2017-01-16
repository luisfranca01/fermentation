from flask import Flask, request, render_template, redirect, url_for
import os
import glob
import sqlite3
import time
import subprocess
#from crontab import CronTab

app = Flask(__name__)

tablename=''

@app.route('/', methods=['POST', 'GET'])
def render_indexHTML():
    global tablename
    dbFiles = getDBtables()
    if not tablename:
        try:
            tablename = dbFiles[0]
        except IndexError:
            return render_template('index.html')
    info = getinfodb()
    return render_template('index.html',
                           dbFiles = dbFiles,
                           tablename=tablename,
                           infotextarea = info)


@app.route('/table', methods=['POST', 'GET'])
def deftablename():
    global tablename
    tablename = str(request.form['drop'])
    return redirect(url_for('render_indexHTML'))

@app.route('/text', methods=['POST', 'GET'])
def submittext():
    global tablename
    text = str(request.form["text"])
    if text:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("INSERT OR REPLACE into '{a}' (id, hora, T1, T2, Tex, info) values ((select id from '{a}' where info is not null), null, null, null, null,'{b}')".format(a=tablename, b=text))
        con.commit()
        con.close()
        return redirect(url_for('render_indexHTML'))

@app.route('/createRun', methods=['POST', 'GET'])
def createRun():
    data = request.form['runName']
    if data:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute('''create table if not exists {table} (id INTEGER PRIMARY KEY, hora datetime, T1 REAL, T2 REAL, Tex REAL, info TEXT);'''.format(table=data))
        con.commit()
        con.close()
        return  redirect(url_for('render_indexHTML'))

def getDBtables():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' ;""")
    files = cursor.fetchall()
    COLUMN = 0
    column=[elt[COLUMN] for elt in files]
    con.close()
    return (sorted(column, reverse=True))


def getinfodb():
    global tablename
    con = sqlite3.connect('database.db')
    con.row_factory = lambda cursor, row: row[0]
    cursor = con.cursor()
    cursor.execute("SELECT info from '{a}' WHERE info is not null;".format(a=tablename))
    files = cursor.fetchone()
    con.close()
    return str(files)

@app.route('/shutdown')
def shutdown():
    # subprocess.call(['shutdown -h now'])
    return ("Shutting down raspberry")


@app.route('/start', methods=['POST', 'GET'])
def managecron():
    data = request.form['refreshID']
    return data
    # tab = CronTab()
    # cmd = '/var/www/pjr-env/bin/python /var/www/PRJ/job.py'
    # cron_job = tab.new(cmd)
    # cron_job.minute().on(0)
    # cron_job.hour().during(09,18)
    # tab.write()
    # return True


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
