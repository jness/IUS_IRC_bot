import socket

class IRC:

    server = "irc.freenode.net"
    channel = "#test"
    botnick = "irc_bot"

    def connect(self):
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.connect((self.server, 6667))
        self.ircsock.send("USER "+ self.botnick +" "+ self.botnick +" "+ self.botnick +" :IUS Notification Bot.\n")
        self.ircsock.send("NICK "+ self.botnick +"\n")
        self.joinchan(self.channel)
        return self.ircsock

    def quit(self):
        self.ircsock.close()

    def joinchan(self, channel):
      self.ircsock.send("JOIN "+ channel +"\n")
    
    def ping(self):
      self.ircsock.send("PONG :pingis\n")

    def post(self, msg):
      self.ircsock.send("PRIVMSG "+ self.channel +" :"+ msg +"\n")

    def sendmsg(self, nick, msg):
      self.ircsock.send("PRIVMSG "+ nick +" :"+ msg +"\n")


