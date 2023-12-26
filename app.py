from flask import Flask, current_app, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)                                              # tells flask app all you need is in current working dir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'      #tells app where DB is located 3 / = relative path 4 is an absolute path
app.config['SQLALCHEMY_BINDS']={
    'credentials': 'sqlite:///credentials.db'
}
db =SQLAlchemy(app)
app.app_context().push()                                         #ensures that you are within the application context when calling db.create_all(

class dbase(db.Model):                                              #Info in DB
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class login(db.Model):
    __bind_key__ = 'credentials'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique= True, nullable= False)
    password = db.Column(db.String(20))

def __repr__(self):
    return '<Task %r>' % self.id        #returns task and its name when a new task is created, %r is placeholder for self.id



@app.route('/', methods=['POST', 'GET'])            # decorater to add more functionality
def index():
    

    if request.method == 'POST':             #index.html form interaction
        task_content = request.form['content']
        new = dbase(content=task_content)

        try:
            db.session.add(new)
            db.session.commit()  
            return redirect('/')            #redirect base to index.html

        except:
                return 'Error adding task'

                                        
    else:
        tasks = dbase.query.order_by(dbase.date_created).all()           #show all task sorted by creation date
        return  render_template('index.html', tasks=tasks)                 
        #return html template to web app

@app.route('/delete/<int:id>')              #flask decoratoer '<>' used to create variable parts in the URL
def delete(id):
    
    ToDelete = dbase.query.get_or_404(id)

    try:
        db.session.delete(ToDelete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'That task cannot be deleted or does not exist'



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task=dbase.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']              #box content will be contents of selected task
    
        try:
            db.session.commit()                        #content was set above so session.add isnt needed
            return redirect('/')

        except:
            return 'The task could not be updated, or does not exist'

    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)                #calling app (flask) to run, can pass in params of where to run (IP) and port

'''
To start db:  python3 > from app import db > db.create_all()
'''


'''@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        if request.form['username'] == login.query.username.filter_by():
            pass'''
    