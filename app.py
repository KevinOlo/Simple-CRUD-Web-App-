from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import wtforms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)                                           # tells flask app all you need is in current working dir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'     #tells app where DB is located 3 / = relative path 4 is an absolute path
#app.config['SQLALCHEMY_BINDS'] = {
    'credentials': 'sqlite:///credentials.db'
}
app.config['SECRET_KEY']='g15classified'             #to secure session cookie
db = SQLAlchemy(app)
app.app_context().push()                                 #ensures that you are within the application context when calling db.create_all()

class dbase(db.Model):                              #Info in DB
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class login(db.Model, UserMixin):
    #__bind_key__ = 'credentials'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class registration(FlaskForm):
   username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw = {'placeholder': 'username'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=80, render_kw={'placeholder': 'password'})])

   submit = SubmitField("Create Account") 

   def validateUser(self, username):
      existingUserName = login.query.filter_by(username=username.data).first()  #.data - where the username column matches the value of username.data. Here, username refers to the form field, and .data is accessing the data submitted with the form. 
      if existingUserName:
         raise ValidationError('Username is already in use, please select a different one')
      

class loginform(FlaskForm):
   username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw = {'placeholder': 'username'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=80, render_kw={'placeholder': 'password'})])

   submit = SubmitField("Login") 

   def validateUser(self, username):
      existingUserName = login.query.filter_by(username=username.data).first()  #.data - where the username column matches the value of username.data. Here, username refers to the form field, and .data is accessing the data submitted with the form. 
      if existingUserName:
         raise ValidationError('Username is already in use, please select a different one')



def __repr__(self):
    return '<Task %r>' % self.id                 #returns task and its name when a new task is created, %r is placeholder for self.id

@app.route('/', methods=['GET'])
def index():
    return redirect('/login/')

@app.route('/login/', methods=['GET', 'POST'])
def login_web():
    if request.method == 'POST':
        username = request.form.get('username', '')              #request.form.get() used to retrieve the values with default values set to empty strings. helps prevent BadRequestKeyError if the keys are not present in the form data.
        password = request.form.get('password', '')

        user_check = login.query.filter_by(username=username).first()

        if user_check and user_check.password == password:
            return f'{username} has entered the Task Manager'
        else:
            return 'Invalid username or password'

    return render_template('login.html')



@app.route('/register/', methods=['POST', 'GET'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check for empty values
    if not username or not password:
        return 'Username and password cannot be empty'

    existing_user = login.query.filter_by(username=request.form.get('username')).first()

    if existing_user:
        return 'Sorry, this username has been taken'
    else:
        newuser = login(username=username, password=password)
        db.session.add(newuser)
        db.session.commit()
        return redirect('/login/')
        return redirect (url_for('login_web') )

    return render_template('register.html')



@app.route('/home/', methods=['POST', 'GET'])            # decorater to add more functionality
def home():


  if request.method == 'POST':                        #index.html form interaction
    task_content = request.form['content']
    new = dbase(content=task_content)

    try:
      db.session.add(new)
      db.session.commit()
      return redirect('/home/')                    #redirect base to index.html

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
    return redirect('/home/')
   except:
    return 'That task cannot be deleted or does not exist'






@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

  task=dbase.query.get_or_404(id)

  if request.method == 'POST':
    task.content = request.form['content']              #box content will be contents of selected task
    
    try:    
      db.session.commit()                        #content was set above so session.add isnt needed
      return redirect('/home/')

    except:
      return 'The task could not be updated, or does not exist'

  else:
    return render_template('update.html', task=task)





if __name__ == '__main__':
  app.run(debug=True)                #calling app (flask) to run, can pass in params of where to run (IP) and port

'''
To start db:  python3 > from app import db > db.create_all()
'''

