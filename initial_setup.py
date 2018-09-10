import couchdb
from werkzeug.security import generate_password_hash, check_password_hash

db = couchdb.Server("http://admin:ashish@localhost:5984/")
d = db.create("users")
dd = db.create("organisations")
da = {"password" : generate_password_hash("admin"), "type":"admin", "email":"admin@ardulous.io", "connections":{'friends':[], 'followers':[], 'following':[]}, "personal":{"dob":"04/01/1999", "address":"", "occupation":"", "interest":""} }
dc = {"password" : generate_password_hash("ashish"), "type":"ashish", "email":"ashish@ardulous.io", "connections":{'friends':[], 'followers':[], 'following':[]}, "personal":{"dob":"04/01/1999", "address":"", "occupation":"", "interest":""} }
d['admin'] = da
d['ashish'] = dc


