import couchdb
import hashlib
import json
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self, url):
        self.db = couchdb.Server(url)
        return 

    def validateUser(self, uid, upass):
        d = self.db
        try: 
            h = d['users'][str(uid)]['password']
            if(check_password_hash(h, upass)):
                return True
            return False
        except:
            return False

    def validateAdmin(self, uid, upass):
        d = self.db
        try: 
            h = d['users'][str(uid)]['password']
            if d['users'][str(uid)]['type'] == 'admin':
                if(check_password_hash(h, upass)):
                    return True
            return False
        except:
            return False

    def makeUser(self, uid, upass):
        d = self.db 
        d['users'][str(uid)] = {'password':generate_password_hash(upass)}
        return 

    def getUserInfo(self, search):
        d = self.db 
        try:
            
            return None
        except:
            return None 
        return None
