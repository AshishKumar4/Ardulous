import string 
from flask import * 
from Database import *
from User import *
from flask_sessionstore import Session
import json

app = Flask(__name__)
app.config.update(
    DATABASE = 'Ardulous'
)
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
#Session(app)

global db  
db = Database("mongodb://localhost:27017/")

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
                ss, st, su, sv = db.searchUser(squery)
                byid = [db.getUserMinInfo(i['_id']) for i in ss]
                byname = [db.getUserMinInfo(i['_id']) for i in st]
                byemail = [db.getUserMinInfo(i['_id']) for i in su]
                bypost = [db.getUserMinInfo(i['_id']) for i in sv]
                return render_template("/internal/search.html", byid = json.dumps({"data":byid, "type":"user"}), byname = json.dumps({"data":byname, "type":"user"}), byemail = json.dumps({"data":byemail, "type":"user"}), bypost = json.dumps({"data":bypost, "type":"post"}))
            except:
                return render_template("/500.html")
            return render_template("/internal/search.html")
        return render_template("/internal/search.html")
    return login_user()


@app.route("/logout", methods=["GET", "POST"])
def logout():
    global db
    del db 
    db = Database("mongodb://localhost:27017/")
    session.pop('login', None)
    session.pop('feedpos', None)
    return redirect("/login_user")#render_template("/login_user.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    global db  
    if "login" in session:
        if request.method == "GET" and request.args.get('user'): # Comment out one of these later request.method == "POST" or 
            try: 
                res = request.args.get('user')
                ss = res#res['user']
                info = db.getUserInfo(ss)
                return render_template("/internal/profile.html", profile_id = ss, profile_cover_location = info['profile_cover'], profile_pic_location = info['profile_pic'], profile_name = info['name'], profile_info = info['info'], profile_residence_link = info['city'], profile_email = info['email'], profile_stats_follower_count = info['stats']['followers'], profile_stats_following_count = info['stats']['following'])    # Pass information of the current user   
            except Exception as e: 
                return render_template("/500.html", error = e)
        ss = session['login'] 
        info = db.getUserInfo(ss)
        return render_template("/internal/profile.html",  profile_id = ss, profile_cover_location = info['profile_cover'], profile_pic_location = info['profile_pic'], profile_name = info['name'], profile_info = info['info'], profile_residence_link = info['city'], profile_email = info['email'], profile_stats_follower_count = info['stats']['followers'], profile_stats_following_count = info['stats']['following'])    # Pass information of the current user
    return redirect("/login_user")



############################################ JavaScript POST Handlers ############################################

@app.route("/handlers/feedfetch", methods=["GET", "POST"])
def feedFetch():
    global db  
    if "login" in session:
        res = request.get_json(force=True)
        count = int(res['count'])
        ss = session['login'] 
        pos = int(res['feedpos'])
        feed = db.popFeeds(ss, pos, count)
        feed.reverse()
        for i in feed:
            uid = i['author-id']
            pp = db.getUserInfo(uid)
            i['author-pic'] = pp["profile_pic"]
            i['author-name'] = pp["name"]
        return jsonify(feed)
    return None

@app.route("/handlers/originalsfetch", methods=["GET", "POST"])
def originalFetch():
    global db  
    if "login" in session:
        res = request.get_json(force=True)
        count = int(res['count'])
        if res['user'] == '':
            ss = session['login'] 
        else:
            ss = res['user']
        pos = int(res['feedpos'])
        feed = db.popOriginals(ss, pos, count)
        pp = db.getUserInfo(ss)
        feed.reverse()
        for i in feed:
            i['author-pic'] = pp["profile_pic"]
            i['author-name'] = pp["name"]
        return jsonify(feed)
    return None

@app.route("/handlers/newpost", methods=['GET', 'POST'])
def newPost():
    global db 
    if "login" in session: 
        ss = session['login']
        post = request.get_json(force=True)
        p = db.createPost(ss, post)
        if p:
            db.pushFeedsToFollowers(ss, p)
            return jsonify("Post created Successfully!")
        else:
            return jsonify("Couldn't make post, internal error")
    return None

@app.route("/handlers/postcomment", methods=['GET', 'POST'])
def postcomment():
    global db 
    if "login" in session:
        ss = session['login']
        pid = request.get_json(force=True)['postid']
        data = request.get_json(force=True)['data']
        p = db.makeCommentPost(ss, pid, data)
        return jsonify(p)
    return None

@app.route("/handlers/postlike", methods=['GET', 'POST'])
def postlike():
    global db 
    if "login" in session:
        ss = session['login']
        pid = request.get_json(force=True)['postid']
        p = db.makeLikePost(ss, pid)
        return jsonify(p)
    return None

@app.route("/handlers/postshare", methods=['GET', 'POST'])
def postshare():
    global db 
    if "login" in session:
        ss = session['login']
        pid = request.get_json(force=True)['postid']
        p = db.makeSharePost(ss, pid)
        return jsonify(p)
    return None

@app.route("/handlers/makefollow", methods=['GET', 'POST'])
def makeFollow():
    global db  
    if "login" in session:
        ss = session['login']
        uid = request.get_json(force=True)['uid']
        if db.makeFollow(ss, uid):
            return jsonify("You are now following the user "+uid+"!")
        return None 
    return None 