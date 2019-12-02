from flask import *
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config['MOMGO_DBNAME']='mydb'
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)
app.secret_key = "dibashthapa"
tasks=[]
@app.route("/")
def home():
    #session['id']=uuid.uuid4()
    if 'Email' in session:
        return render_template("index.html")
       
    else:
        return render_template("login.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        details = request.form
        Email = details['Email']
        Password = details['Password']
        account=mongo.db.Users
        existing_account = account.find_one({"email":Email,"password":Password})
        if(existing_account is None):
            return "Incorrect information!" 
        else:
            session['Email']=Email
            return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        details=request.form
        Email = details['Email']
        Password = details['Password']
        Name=details['Name']
        account=mongo.db.Users
        existing_account = account.find_one({"name":Name,"email":Email})
        if existing_account is None:
            mongo.db.Users.insert_one({"name":Name,"email":Email,"password":Password,"tasks":"none"})
            return redirect(url_for("login"))
        else:
            return "sorry user already registered"  
    else:
        return render_template("register.html")
@app.route("/add",methods=['GET','POST'])
def add_task():
    if 'Email' in session:
        if request.method=='POST':
            task=request.form['task']
            tasks.append(task)
            myquery = { "email":session['Email']}
            newvalues = { "$set": {"tasks":tasks} }
            mongo.db.Users.update_one(myquery,newvalues)
            db_query=mongo.db.Users.find({},{'tasks':tasks})
            db_tasks=db_query[0]
            return render_template("index.html",tasks=db_tasks['tasks'])
        else:
            return render_template("index.html")
            
@app.route("/logout",methods=['GET','POST'])
def logout():
    if request.method=="POST":
        for key in session.keys():
            session.pop(key)
            return redirect(url_for("login"))
    else:
        return redirect(url_for("home"))
if __name__=='__main__':
    app.run(debug=True)