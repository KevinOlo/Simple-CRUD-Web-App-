from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # tells flask app all you need is in the current working dir
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # tells app where DB is located 3 / = relative path 4 is an absolute path
app.config["SQLALCHEMY_BINDS"] = {"credentials": "sqlite:///credentials.db"}
app.secret_key = 'raw_key'
db = SQLAlchemy(app)
app.app_context().push()  # ensures that you are within the application context when calling db.create_all()

class login(db.Model):
  __bind_key__ = "credentials"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True, nullable=False)
  password = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

class dbase(db.Model):  # Info in DB
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  '''user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
  user = db.relationship('login', backref=db.backref('tasks', lazy=True))'''
  

def __repr__(self):
  return ("<Task %r>" % self.id)  # returns task and its name when a new task is created, %r is a placeholder for self.id


@app.route("/", methods=["GET"])
def homepage():
  return render_template('home.html')


'''@app.route('/home/', methods=['GET', 'POST'])
def index(): 
  return render_template('index.html')'''



@app.route("/login/", methods=["GET", "POST"])
def login_web():
  if request.method == "POST":
    username = request.form.get("username", "")  # request.form.get() used to retrieve the values with default values set to empty strings. helps prevent BadRequestKeyError if the keys are not present in the form data.
    password = request.form.get("password", "")

    user_check = login.query.filter_by(username=username).first()

    if user_check and user_check.password == password:
      print (f"{username} has entered the Task Manager")
      session['login'] = True
      session['username'] = username
      return redirect('/home/')
    else:
      return "Invalid username or password"

  return render_template("login.html")


@app.route('/logout/', methods=['GET'])
def logout():
  session.clear()
  return redirect('/')



@app.route("/register/", methods=["POST", "GET"])
def register():
  
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

        # Check for empty values
    if not username or not password or not email:
      return "Username and password and email cannot be empty"

    existing_user = login.query.filter_by(username=username).first()
    existing_email = login.query.filter_by(email=email).first()


    if existing_user:
      return "Sorry, this username has been taken"
    elif existing_email:
      return "This email is already in use"
    else:
      newuser = login(username=username, password=password, email=email)
      db.session.add(newuser)
      db.session.commit()
    
      return redirect('/registration_success/')   

  return render_template('register.html')



@app.route('/registration_success/', methods=['POST'])
def registration_success():
  return redirect('/registration_success/')



@app.route('/home/', methods=['POST', 'GET'])  # decorator to add more functionality
def home():

  if session.get('login'):
    if request.method == 'POST':  # index.html form interaction
      task_content = request.form['content']
      new = dbase(content=task_content)

      try:
        db.session.add(new)
        db.session.commit()
        return redirect('/index/')  # redirect base to index.html

      except:
        return 'Error adding task'

    else:
      tasks = dbase.query.order_by(dbase.date_created).all()  # show all tasks sorted by creation date
      return render_template('index.html', tasks=tasks)
      # return html template to web app

  else:
    return 'Please login'
    #return redirect('/login/')


@app.route('/delete/<int:id>')  # flask decorator '<>' used to create variable parts in the URL
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

  task = dbase.query.get_or_404(id)

  if request.method == 'POST':
    task.content = request.form['content']  # box content will be contents of the selected task

    try:
      db.session.commit()  # content was set above so session.add isn't needed
      return redirect('/home/')

    except:
      return 'The task could not be updated, or does not exist'

  else:
    return render_template('update.html', task=task)


if __name__ == '__main__':
  app.run(debug=True)  # calling app (flask) to run, can pass in params of where to run (IP) and port

'''
To start db:  python3 > from app import db > db.create_all()
'''