import pymongo
from bson.objectid import ObjectId
import hashlib
import json
from werkzeug.security import generate_password_hash, check_password_hash

import re

def getAge(date):
    return 19

class Database:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client['default']
        return 

    def createUser(self, data, type = "normaluser"):
        d = self.db 
        try:
           # b = d['users'][data['id']]
            dd = {"_id":data['id'], "password" : generate_password_hash(data['password']), "type":type, "email":data['email'], "feed": [], "originals":[], "connections":{'friends':[], 'followers':[], 'following':[]}, "personal":{"profile_pic":data['profile_pic'], "profile_cover":data['profile_cover'], "name": data['name'], "info": data['info'], "dob":data['dob'], "city": data['address']['city'], "address":data['address'], "occupation":data['occupation'], "interest":data['interest']} }
            d['user'].insert_one(dd)
        except:
            return False 
        return False

    def validateUser(self, uid, upass):
        d = self.db
        try: 
            h = d['users'].find_one({"_id":uid})['password']
            if(check_password_hash(h, upass)):
                return True
            return False
        except:
            return False

    def validateAdmin(self, uid, upass):
        d = self.db
        try: 
            h = d['users'].find_one({"_id":uid})['password']
            if d['users'].find_one({"_id":uid})['type'] == 'admin':
                if(check_password_hash(h, upass)):
                    return True
            return False
        except:
            return False

    def searchUser(self, search):
        d = self.db 
        try:
            b = d['users']
            reg = re.compile("\\b"+search+"\\b", re.IGNORECASE)
            #Search through direct id ->
            gg = b.find({"_id":reg}, {"_id":1})
            #Search through direct name ->
            gh = b.find({"personal.name":reg}, {"_id":1})
            #Search through direct Posts ->
            gj = b.find({"_id":reg}, {"_id":1})
            #Search through direct email ->
            reg = re.compile("[a-z]*"+search+"[a-z]*", re.IGNORECASE)
            gi = b.find({"email":reg}, {"_id":1})
            return gg, gh, gi, gj
        except:
            return None 
        return None

    def getUserInfo(self, uid):
        d = self.db 
        info = {}
        try:
            b = d['users'].find_one({"_id":uid})
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

    def getUserMinInfo(self, uid):
        d = self.db 
        info = {}
        try:
            b = d['users'].find_one({"_id":uid})
            #info['email'] = b['email']
            info['id'] = b['_id']
            info['city'] = b['personal']['city']
            info['age'] = getAge(b['personal'])
            info['info'] = b['personal']['info']
            info['name'] = b['personal']['name']
            info['profile_pic'] = b['personal']['profile_pic']  
            #info['profile_cover'] = b['personal']['profile_cover']
            info['stats'] = {}
            info['stats']['followers'] = len(b['connections']['followers'])
            info['stats']['following'] = len(b['connections']['following'])
            info['stats']['posts'] = len(b['originals'])
            return info
        except:
            return None 
        return None

    def getProfilePic(self, uid):
        return ""

    def popOriginals(self, uid, pos, count):
        d = self.db 
        feed = []
        try:
            b = d['users'].find_one({"_id":uid})
            # Every user should have a Feeds List, pop values from it 
            fl = list(b['originals'])
            o = len(fl)
            if pos == o :
                return None
            feed = fl[(o-pos)-min([o,count]):o - pos]
            g = list()
            for i in feed:
                j = dict(d['posts'].find_one({'_id':ObjectId(i)}))
                j['post-id'] = i 
                j['_id'] = i
                j['likes'] = len(j['stats']['likes'])
                g.append(j)
            return g
        except: 
            return None 
        return None 

    def popFeeds(self, uid, pos, count):
        d = self.db 
        feed = []
        try:
            b = d['users'].find_one({"_id":uid})
            # Every user should have a Feeds List, pop values from it 
            fl = list(b['feed'])
            o = len(fl)
            if pos == o :
                return None
            feed = fl[(o-pos)-min([o,count]):o - pos]
            g = list()
            for i in feed:
                j = dict(d['posts'].find_one({'_id':ObjectId(i)}))
                j['post-id'] = i 
                j['_id'] = i
                j['likes'] = len(j['stats']['likes'])
                g.append(j)
            return g
        except: 
            return None 
        return None 

    def pushFeed(self, uid, postid):    # Puts a post into a given user's feed
        d = self.db 
        try:
            b = d['users'].find_one({"_id":uid})
            fl = b['feed']
            fl.append(postid)
            b['feed'] = fl   
            d['users'].save(b)
            #d['users'].commit()
            return True
        except: 
            return None 
        return None 

    def createPost(self, uid, postdata):    # creates a new post
        d = self.db 
        try:
            p = d['posts']
            pp = {"text":postdata['text'], "author-id":uid, "time":postdata['time'], "stats":{"likes":[], "comments":[], "shares":[]}}
            pid = str(p.save(pp))

            b = d['users'].find_one({"_id":uid})
            fl = b['originals']
            fl.append(pid)
            b['originals'] = fl   
            #d['users'].save(b)
            #d['users'].commit()

            #b = d['users'].find_one({"_id":uid})   ## Push this post into the feed of the creator as well
            fl = b['feed']
            fl.append(pid)
            b['feed'] = fl   
            d['users'].save(b)
            #d['users'].commit()
            return pid
        except: 
            return None 
        return None 

    def pushFeedsToFollowers(self, uid, pid):
        d = self.db 
        try: 
            b = d['users'].find_one({"_id":uid})
            followers = b['connections']['followers']
            #l = [d['users'][i] for i in followers]
            for i in followers:
                self.pushFeed(i, pid)
        except: 
            return None 
        return None


    def makeCommentPost(self, uid, pid, data):
        d = self.db 
        try:
            b = d['users'].find_one({"_id":uid})
            # Add this post as 'Liked' post for the user
            # and add a like on the post itself
            p = d['posts'].find_one({"_id":ObjectId(pid)})
            k = p['stats']['comments']
            k.append(dict({"id":uid, "data":data}))
            p['stats']['comments'] = k 
            d['posts'].save(p)
            return len(k)
        except:
            return None

    def makeLikePost(self, uid, pid):
        d = self.db 
        try:
            b = d['users'].find_one({"_id":uid})
            # Add this post as 'Liked' post for the user
            # and add a like on the post itself
            p = d['posts'].find_one({"_id":ObjectId(pid)})
            k = p['stats']['likes']
            if uid not in k:
                k.append(uid)
                p['stats']['likes'] = k 
                d['posts'].save(p)
                #d['posts'].commit()
            else: 
                pass
            return len(k)
        except:
            return None

    def makeSharePost(self, uid, pid):
        d = self.db 
        try:
            b = d['users'].find_one({"_id":uid})
            # Add this post as 'Liked' post for the user
            # and add a like on the post itself
            p = d['posts'].find_one({"_id":ObjectId(pid)})
            k = p['stats']['likes']
            if uid not in k:
                k.append(uid)
                p['stats']['likes'] = k 
                d['posts'].save(p)
                #d['posts'].commit()
            else: 
                pass
            return len(k)
        except:
            return None

    def makeFollow(self, byfollowid, tofollowid):
        d = self.db 
        try: 
            b = d['users'].find_one({"_id":byfollowid})
            t = d['users'].find_one({"_id":tofollowid})
            # User B wants to follow User T
            
            bc = b['connections']
            tc = t['connections']
            bc['following'].append(tofollowid)
            tc['follower'].append(byfollowid)

            if tofollowid in bc['follower']:
                # If they both follow each other, make them each other's friends!
                tc['friends'].append(byfollowid)
                bc['friends'].append(tofollowid)

            b['connections'] = bc 
            t['connections'] = tc 
            d['users'].save(b)
            d['users'].save(t)
            return True
        except:
            return None 