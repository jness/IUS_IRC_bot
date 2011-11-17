#!/usr/bin/env python
from datetime import datetime
from time import sleep
from multiprocessing import Process

from _lib_irc import *
from _lib_launchpad import fetchtask
from _lib_script import run

irc = IRC()
irc.server = "irc.freenode.net"
irc.channel = "#iuscommunity"
irc.botnick = 'iusbot'

# Lets give it some time to connect
print 'Running IRC Bot'
ircsock = irc.connect()

# Our Process that listen for messages
class IRCbot(Process):
    def run(self):
        while True:
            ircmsg = ircsock.recv(2048)
            ircmsg = ircmsg.strip('\n\r')

            # If this was a message it should have a channel
            # Else this was a server type and we dont care
            try:
                channel = ircmsg.split()[2]
                type = ircmsg.split()[1]
            except IndexError:
                channel = None
                type = None
            
            # If server pings us we nee to pong
            if ircmsg.find("PING :") != -1:
                irc.ping()

            if ircmsg:
                # If we recieve a message in channel
                if ircmsg.find(":"+ irc.botnick) != -1:
                    try:
                        command = ircmsg.split()[4]
                    except IndexError:
                        continue

                    try:
                        subcommand = ircmsg.split()[5]
                    except IndexError:
                        subcommand = ''

                    attempt = run(command, subcommand)
                    if attempt:
                        results = attempt.communicate()
                        if not results[1]:
                            results = results[0]
                            results = results.split('\n')
                            for lines in results:
                                irc.post(str(lines))
                            print 'running', command

                # If we recieved a private message
                if channel == irc.botnick and type == 'PRIVMSG': 
                    
                    # Check for subcommand otherwise set it blank
                    try:
                        subcommand = ircmsg.split()[4]
                    except IndexError:
                        subcommand = ''

                    try:
                        command = ircmsg.split()[3]
                        command = command.strip(':')
                        nick = ircmsg.split('!')[0]
                        nick = nick.strip(':')

                        attempt = run(command, subcommand)
                        if attempt:
                            results = attempt.communicate()
                            if not results[1]:
                                print 'running', command, 'for', nick
                                results = results[0]
                                results = results.split('\n')
                                for lines in results:
                                    irc.sendmsg(nick, str(lines))
                        else:
                            print 'invalid command requested by',  nick + '. command was', command
                            irc.sendmsg(nick, command + ' is not a valid script')
                    except IndexError:
                        pass
                            

# Our process that check LP for new tickets or updates every 10minutes
def lpsearch(lastupdate):
    now = datetime.utcnow()

    print '[' + now.ctime() + '] Running Launchpad Check'
    respond = []

    for task in fetchtask():
        print ' checking ' + str(task.bug.id)
        print '    lastupdate:', lastupdate.ctime()
        print '    ticket created:', task.date_created.ctime()
        if lastupdate < task.date_created.replace(tzinfo=None):
            respond.append("NEW BUG: " + task.title)
            lastupdate = now

        last_message = len(task.bug.messages) - 1
        date_last_message = task.bug.messages[last_message].date_created
        if task.date_created != date_last_message:
            print '    ticket updated:', date_last_message.ctime()
            if lastupdate < date_last_message.replace(tzinfo=None):
                respond.append("BUG UPDATE: " + task.title)
                lastupdate = now

    if respond:
        for message in respond:
            print message
            irc.post(message)

    return lastupdate

def main():
    IRCbot().start()

    lastupdate = datetime.utcnow()

    while True:
        time = datetime.now()
        if time.minute in [0,10,20,30,40,50]:
            lastupdate = lpsearch(lastupdate)
            sleep(60)

if __name__ == '__main__':
    main()
