import couchdb
from werkzeug.security import generate_password_hash, check_password_hash

db = couchdb.Server("http://admin:ashish@localhost:5984/")
d = db.create("users")
dd = db.create("organisations")
dd = db.create("posts")
da = {"password" : generate_password_hash("admin"), "type":"admin", "email":"admin@ardulous.io", "feed": [], "originals":[], "connections":{'friends':["ashish"], 'followers':["ashish"], 'following':["ashish"]}, "personal":{"profile_pic":"/static/img/Users/ashish/profile_pic.jpg", "profile_cover":"/static/img/Users/ashish/profile_cover.jpg", "name": "Administrator", "info": "I am the god of this realm! Thou shall bent ye knee!", "dob":"04/01/1999", "city": "Atlantis", "address":"", "occupation":"", "interest":""} }
dc = {"password" : generate_password_hash("ashish"), "type":"ashish", "email":"ashish@ardulous.io", "feed": [], "originals":[], "connections":{'friends':["admin"], 'followers':["admin"], 'following':["admin"]}, "personal":{"profile_pic":"/static/img/Users/ashish/profile_pic.jpg", "profile_cover":"/static/img/Users/ashish/profile_cover.jpg", "name": "Ashish Kumar Singh", "info": "I am the Human form of the god of this realm! Thou shall bent ye knee!", "dob":"04/01/1999", "city":"New Delhi","address":"", "occupation":"", "interest":""} }
d['admin'] = da
d['ashish'] = dc

dd['test'] = {"text":"test", "author-id":"admin", "time":"00", "stats":{"likes":[], "comments":[], "shares":[]}}


