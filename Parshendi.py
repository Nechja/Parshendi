import re
import socket
from playsound import playsound

HOST = "irc.twitch.tv"                          
PORT = 6667
##Please fill this out with your info
CHAN = "#YOURCHANNELNAME"
NICK = "YOURBOTNAME"
PASS = "oauth:ADD YOUR OAUTH HERE"

##IRC Chat basic stuff

def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

#sender parce
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result

##message loading
def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result

##Message parcing
def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {}
        if msg[0] in options:
            options[msg[0]]()

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message)

                    print(sender + ": " + message)
                    ##make sure you have an MP3 in the same folder
                    playsound('twitchsound.mp3')

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")