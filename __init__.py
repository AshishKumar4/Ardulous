import string 
import couchdb 
from flask import * 
from Database import *
from User import *
from flask_sessionstore import Session


app = Flask(__name__)
app.config.update(
    DATABASE = 'Ardulous'
)
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
#Session(app)

global db  
db = Database("http://admin:ashish@localhost:5984")

# Set the secret key to some random bytes. Keep this really secret!
import os 
import random
app.secret_key = os.urandom(32)#bytes(str(hex(random.getrandbits(128))), 'ascii')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("/404.html")

@app.route("/home", methods=["GET", "POST"])    # Future Home Page
def home():
    return render_template('/home.html')

@app.route("/", methods=["GET", "POST"])        # Home Page
@app.route("/login_user", methods=["GET", "POST"])
def login_user():
    if "login" in session:
        return dashboard()
    elif request.method == "POST":
        try:
            uid = request.form['id']
            upass = request.form['pw']
            if db.validateUser(uid, upass):
                session["login"] = uid
                session["feedpos"] = 0
                #session["database"] = Database("http://admin:ashish@localhost:5984")
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
    if "login" in session: 
        if request.method == "POST":
            #pp = request.form[]
            return render_template('/internal/home.html')
        ss = session['login'] 
        info = db.getUserInfo(ss)
        return render_template('/internal/home.html', profile_cover_location = info['profile_cover'], profile_pic_location = info['profile_pic'], profile_name = info['name'], profile_info = info['info'], profile_residence_link = info['city'], profile_email = info['email'], profile_stats_follower_count = info['stats']['followers'], profile_stats_following_count = info['stats']['following'])    # Pass information of the current user
    else:
        return redirect("/login_user")
    return render_template('/500.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    if "login" in session:
        if request.method == "POST":
            try: 
                squery = request.form['search']
                global db
                ss = db.searchUser(squery)
                return render_template("/internal/search.html")
            except:
                return render_template("/500.html")
            return render_template("/internal/search.html")
        return render_template("/internal/search.html")
    return login_user()


@app.route("/logout", methods=["GET", "POST"])
def logout():
    global db
    del db 
    db = Database("http://admin:ashish@localhost:5984")
    session.pop('login', None)
    session.pop('feedpos', None)
    return redirect("/login_user")#render_template("/login_user.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    global db  
    if "login" in session:
        if request.method == "POST":
            try: 
                ss = request.form['id']
                info = db.getUserInfo(ss)
                return render_template("/internal/profile.html", profile_cover_location = info['profile_cover'], profile_pic_location = info['profile_pic'], profile_name = info['name'], profile_info = info['info'], profile_residence_link = info['city'], profile_email = info['email'], profile_stats_follower_count = info['stats']['followers'], profile_stats_following_count = info['stats']['following'])    # Pass information of the current user   
            except: 
                return render_template("/500.html")
        ss = session['login'] 
        info = db.getUserInfo(ss)
        return render_template("/internal/profile.html", profile_cover_location = info['profile_cover'], profile_pic_location = info['profile_pic'], profile_name = info['name'], profile_info = info['info'], profile_residence_link = info['city'], profile_email = info['email'], profile_stats_follower_count = info['stats']['followers'], profile_stats_following_count = info['stats']['following'])    # Pass information of the current user
    return redirect("/login_user")



############################################ JavaScript POST Handlers ############################################

@app.route("/handlers/feedfetch", methods=["GET", "POST"])
def feedFetch():
    global db  
    if "login" in session:
        count = 5#request.form['count']
        ss = session['login'] 
        pos = session['feedpos']
        session['feedpos'] = pos
        feed = db.popFeeds(ss, pos, count)
        feed.reverse()
        for i in feed:
            uid = i['author-id']
            pp = db.getUserInfo(uid)
            i['author-pic'] = pp["profile_pic"]
            i['author-name'] = pp["name"]
        pos += count
        return jsonify(feed)
    return None

@app.route("/handlers/newpost", methods=['GET', 'POST'])
def newPost():
    global db 
    if "login" in session: 
        ss = session['login']
        post = request.get_json(force=True)
        if db.createPost(ss, post):
            return jsonify("Post created Successfully!")
        else:
            return jsonify("Couldn't make post, internal error")
    return None