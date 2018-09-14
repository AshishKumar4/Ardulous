import couchdb
import hashlib
import json
from werkzeug.security import generate_password_hash, check_password_hash

def getAge(date):
    return 19

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

    def searchUser(self, search):
        d = self.db 
        try:
            
            return None
        except:
            return None 
        return None

    def getUserInfo(self, uid):
        d = self.db 
        info = {}
        try:
            b = d['users'][str(uid)]
            info['email'] = b['email']
            info['city'] = b['personal']['city']
            info['age'] = getAge(b['personal'])
            info['info'] = b['personal']['info']
            info['name'] = b['personal']['name']
            info['profile_pic'] = b['personal']['profile_pic']  
            info['profile_cover'] = b['personal']['profile_cover']
            info['stats'] = {}
            info['stats']['followers'] = len(b['connections']['followers'])
            info['stats']['following'] = len(b['connections']['following'])
            return info
        except:
            return None 
        return None

    def getProfilePic(self, uid):
        return ""

    def popFeeds(self, uid, pos, count):
        d = self.db 
        feed = []
        try:
            b = d['users'][str(uid)]
            # Every user should have a Feeds List, pop values from it 
            fl = list(b['feed'])

            feed = fl[(len(fl)-pos)-count:len(fl) - pos]
            p = d['posts']
            g = [p[i] for i in feed]
            return g
        except: 
            return None 
        return None 

    def pushFeed(self, uid, postid):    # Puts a post into a given user's feed
        d = self.db 
        try:
            b = d['users'][str(uid)]
            fl = b['feed']
            fl.append(postid)
            b['feed'] = fl   
            d['users'].save(b)
            d['users'].commit()
            return True
        except: 
            return None 
        return None 

    def createPost(self, uid, postdata):    # creates a new post
        d = self.db 
        try:
            p = d['posts']
            pp = {"text":postdata['text'], "author-id":uid, "time":postdata['time'], "stats":{"likes":[], "comments":[], "shares":[]}}
            pid, prev = p.save(pp)

            b = d['users'][str(uid)]
            fl = b['originals']
            fl.append(pid)
            b['originals'] = fl   
            d['users'].save(b)
            d['users'].commit()

            b = d['users'][str(uid)]    ## Push this post into the feed of the creator as well
            fl = b['feed']
            fl.append(pid)
            b['feed'] = fl   
            d['users'].save(b)
            d['users'].commit()
            return True
        except: 
            return None 
        return None 