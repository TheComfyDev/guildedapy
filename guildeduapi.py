import requests
import uuid
import socketio

io = socketio.Client()

genuuid = uuid.uuid1

base_url = "https://www.guilded.gg/api/"

cookiejar = None

class Team:
    def __init__(self,teamdict):
        td = teamdict
        self.id = td["id"]
        self.name = td["name"]
        self.channels = []
        for channel in requests.get(f"{base_url}/teams/{self.id}/channels", cookies=cookiejar).json()["channels"]:
            self.channels.append(Channel(channel))
        self.subdomain = td["subdomain"]
        #self.bio = td["bio"]
        self.icon = td["profilePicture"]
        self.ownerId = td["ownerId"]

    def  __repr__(self):
        return str({
            "id":self.id,
            "name":self.name,
            "channels":self.channels,
            "subdomain":self.subdomain,
            "icon":self.icon,
            "ownerId":self.ownerId
        })

class Channel:
    def __init__(self,channeldict):
        cd = channeldict
        self.id = cd["id"]
        self.type = cd["type"]
        self.name = cd["name"]
        self.parentChannelId = cd["parentChannelId"]
        self.description = cd["description"]
        self.contentType = cd["contentType"]
        self.groupId = cd["groupId"]

    def  __repr__(self):
        return str({
            "id":self.id,
            "name":self.name,
            "type":self.type,
            "parentChannelId": self.parentChannelId,
            "description": self.description,
            "contentType": self.contentType,
            "groupId": self.groupId
        })

    def send(self,message):
        msgdict = {
            "messageId": str(genuuid()),
            "content": {
                "object": "value",
                "document": {
                    "object":"document",
                    "data": {},
                    "nodes": [
                        {
                            "object":"block",
                            "type":"paragraph",
                            "data":{},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                        "object": "leaf",
                                        "text": message,
                                        "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
        requests.post(f"{base_url}/channels/{self.id}/messages", cookies=cookiejar, json=msgdict)

class MsgChannel:
    def __init__(self,msg):
        self.id=msg["channelId"]
    
    def send(self,message):
        msgdict = {
            "messageId": str(genuuid()),
            "content": {
                "object": "value",
                "document": {
                    "object":"document",
                    "data": {},
                    "nodes": [
                        {
                            "object":"block",
                            "type":"paragraph",
                            "data":{},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                        "object": "leaf",
                                        "text": message,
                                        "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
        requests.post(f"{base_url}/channels/{self.id}/messages", cookies=cookiejar, json=msgdict)

class Bot:
    def __init__(self,prefix=">>"):
        self.prefix = prefix
        self.cmds = {}

    def login(self,email,password):
        global cookiejar
        logindict = {'email':email,'password':password}
        self.loginres = requests.post(base_url+"login", json=logindict)
        self.cookie = self.loginres.headers["Set-Cookie"]
        cookiejar = self.loginres.cookies
        self.userdict = self.loginres.json()["user"]
        print(f"Logged in as {self.userdict['name']}")
        self.medict = requests.get(base_url + "me", cookies=cookiejar).json()
        self.teams = []
        for team in self.medict["teams"]:
            self.teams.append(Team(team))
        io.connect("wss://api.guilded.gg/socket.io?jwt=undefined&guildedClientId=lolnou&EIO=3",headers={"cookie":self.cookie},transports="websocket")

    def on_chat_message(self,func):
        @io.on("ChatMessageCreated")
        def wrapper1(message):
            msgchan = MsgChannel(message)
            content = message["message"]["content"]["document"]["nodes"][0]["nodes"][0]["leaves"][0]["text"]
            if message["message"]["createdBy"] != self.userdict["id"]:
                func(msgchan,content)
        return wrapper1

    def command(self,func):
        self.cmds[func.__name__] = func
        @io.on("ChatMessageCreated")
        def omgwrapper(message):
            msgchan = MsgChannel(message)
            args = message["message"]["content"]["document"]["nodes"][0]["nodes"][0]["leaves"][0]["text"]
            if message["message"]["createdBy"] != self.userdict["id"] and args.startswith(self.prefix):
                args = args.replace(self.prefix,"")
                args = args.split()
                cmd = args[0]
                args.pop(0)
                try:
                    self.cmds[cmd](msgchan,*args)
                except:
                    pass
        return omgwrapper