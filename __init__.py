import string 
import couchdb 
from flask import * 
from Database import *
from User import *

app = Flask(__name__)
app.config.update(
    DATABASE = 'Ardulous'
)
#db = couchdb.Server("http://localhost:5984/")[app.config["DATABASE"]]
global db
global login

db = Database("http://admin:ashish@localhost:5984")
login = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template("/404.html")

@app.route("/home", methods=["GET", "POST"])    # Future Home Page
def home():
    return render_template('/home.html')

@app.route("/", methods=["GET", "POST"])        # Home Page
@app.route("/login_user", methods=["GET", "POST"])
def login_user():
    global db  
    global login 
    if login:
        return dashboard()
    elif request.method == "POST":
        try:
            uid = request.form['id']
            upass = request.form['pw']
            if db.validateUser(uid, upass):
                login = True
                return redirect("/dashboard")
            else:
                return "Incorrect Username/Password"
        except Exception as ex:
            print(ex)
            return render_template("/500.html")
    return render_template('/login_user.html')

@app.route("/login_org", methods=["GET", "POST"])
def login_org():
    return render_template('/login_org.html')

@app.route("/login_admin", methods=["GET", "POST"])
def login_admin():
    global db  
    global login 
    if login:
        return dashboard()
    elif request.method == "POST":
        try:
            uid = request.form['id']
            upass = request.form['pw']
            if db.validateAdmin(uid, upass):
                login = True
                return redirect("/dashboard")
            else:
                return "Incorrect Username/Password"
        except Exception as ex:
            print(ex)
            return render_template("/500.html")
    return render_template('/login_admin.html')

@app.route("/register_org", methods=["GET", "POST"])
def register_org():
    return render_template('/register_org.html')

@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    return render_template('/register_user.html')

############################################ Dashboard and internal stuffs ############################################

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    global db
    global login
    if login: 
        if request.method == "POST":
            #pp = request.form[]
            return render_template('/internal/home.html')
        return render_template('/internal/home.html')
    else:
        return login_user()
    return render_template('/500.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    global db  
    global login 
    if login:
        if request.method == "POST":
            try: 
                squery = request.form['search']
                ss = db.getUserInfo(squery)
                return render_template("/internal/search.html")
            except:
                return render_template("/500.html")
            return render_template("/internal/search.html")
        return render_template("/internal/search.html")
    return login_user()


@app.route("/logout", methods=["GET", "POST"])
def logout():
    global db
    global login 
    login = False 
    del db 
    db = Database("http://admin:ashish@localhost:5984")
    return redirect("/login_user")#render_template("/login_user.html")