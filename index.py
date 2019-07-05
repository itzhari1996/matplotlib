from flask import Flask,render_template,request,redirect
import sqlite3
from datetime import datetime

app=Flask("__name__")

def conndb(query):
    with sqlite3.Connection('test.db') as conn:
        c=conn.cursor()
        data=c.execute(query)
        conn.commit()
    data=data.fetchall()
    return data

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST' and request.form['content']!='':
        content=request.form['content']
        try:
            query='INSERT INTO todo(content) VALUES ("'+content+'");'
            conndb(query)
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        query='SELECT * FROM todo ORDER BY date_created DESC;'
        data=conndb(query)
        return render_template('index.html',data=data)

@app.route('/delete/<int:id>')
def deletetask(id):
    try:
        query='DELETE FROM todo WHERE id='+str(id)
        conndb(query)
        return redirect('/')
    except:
        return 'There was an issue in deleting the task from DB'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        query='update todo set content="'+request.form['content']+'" WHERE id='+str(id)
        try:
           conndb(query)
           return redirect('/')
        except:
            return 'There was an issue in updating the task details in DB'
    else:
        query='select * from todo where id='+str(id)
        tasktoupdate=conndb(query)
        return render_template('update.html',data=tasktoupdate[0])

if __name__=='__main__':
    app.run(debug=True)
