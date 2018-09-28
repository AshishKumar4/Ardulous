import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

db = pymongo.MongoClient("mongodb://localhost:27017/")
df = db['default']  # Create Database

d = df['users']     # Create Collections
dd = df["organisations"]
dd = df["posts"]


da = {"_id": "admin", "password": generate_password_hash("admin"), "type": "admin", "email": "admin@ardulous.io", "feed": [], "originals": [], "connections": {'friends': ["ashish"], 'followers': ["ashish"], 'following': ["ashish", "divyanshi", "anushka"]}, "personal": {
    "profile_pic": "/static/img/Users/ashish/profile_pic.jpg", "profile_cover": "/static/img/Users/ashish/profile_cover.jpg", "name": "Administrator", "info": "I am the god of this realm! Thou shall bent ye knee!", "dob": "04/01/1999", "city": "Atlantis", "address": "", "occupation": "", "interest": ""}}
dc = {"_id": "ashish", "password": generate_password_hash("ashish"), "type": "normaluser", "email": "ashish@ardulous.io", "feed": [], "originals": [], "connections": {'friends': ["admin", "divyanshi", "anushka"], 'followers': ["admin", "divyanshi", "anushka"], 'following': ["admin", "anushka", "divyanshi"]}, "personal": {"profile_pic": "/static/img/Users/ashish/profile_pic.jpg",
                                                                                                                                                                                                                                                           "profile_cover": "/static/img/Users/ashish/profile_cover.jpg", "name": "Ashish Kumar Singh", "info": "I am the Human form of the god of this realm! Thou shall bent ye knee!", "dob": "04/01/1999", "city": "New Delhi", "address": "", "occupation": "", "interest": ""}}

dg = {"_id": "divyanshi", "password": generate_password_hash("divyanshi"), "type": "normaluser", "email": "divyanshi@ardulous.io", "feed": [], "originals": [], "connections": {'friends': ["ashish", "anushka"], 'followers': ["ashish", "anushka", "admin"], 'following': ["ashish", "anushka"]}, "personal": {
    "profile_pic": "/static/img/Users/divyanshi/profile_pic.jpg", "profile_cover": "/static/img/Users/divyanshi/profile_cover.jpg", "name": "Divyanshi Kamra", "info": "I am a cute panda :p ", "dob": "04/01/1999", "city": "M Bhool gyi", "address": "", "occupation": "", "interest": ""}}
dh = {"_id": "anushka", "password": generate_password_hash("anushka"), "type": "normaluser", "email": "anushka@ardulous.io", "feed": [], "originals": [], "connections": {'friends': ["ashish", "divyanshi"], 'followers': ["admin", "ashish", "divyanshi"], 'following': ["ashish", "divyanshi"]}, "personal": {"profile_pic": "/static/img/Users/anushka/profile_pic.jpg",
                                                                                                                                                                                                                                                           "profile_cover": "/static/img/Users/anushka/profile_cover.jpg", "name": "Anushka Gupta", "info": "I am a mature nerd from luckhnow;_; ", "dob": "04/01/1999", "city": "Lucknow", "address": "", "occupation": "", "interest": ""}}
d.insert(da)   # Create four default users
d.insert(dc)   # Create four default users
d.insert(dg)   # Create four default users
d.insert(dh)   # Create four default users

tt = {"_id": "test", "text": "test", "author-id": "admin", "time": "00",
      "stats": {"likes": [], "comments": [], "shares": []}}

dd.insert_one(tt)


