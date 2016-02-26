#bot.py
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import time
import random
import sys
import re
import string
import config
import json

import usercommands

from db_manager import Db_Manager
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2


readbuffer = ""
MOTD = False
version = "0.3"
point_timer = int(round(time.time() * 1000))

#DB
db_manager = Db_Manager(config.CHAN)

#Grabs the user JSON list from twitch servers
def get_user_json():
	try:
		url = "http://tmi.twitch.tv/group/user/" + config.CHAN + "/chatters"
		response = urllib2.urlopen(url)
		data = json.loads(response.read().decode())
		return data["chatters"]["viewers"]
	except:
		print("Error getting JSON from user list")
		return False

def get_moderator_json():
	try:
		url = "http://tmi.twitch.tv/group/user/" + config.CHAN + "/chatters"
		response = urllib2.urlopen(url)
		data = json.loads(response.read().decode())
		return data["chatters"]["moderators"]
	except:
		print("Error getting JSON from user list")
		return False

def add_points():
	db_manager.query("UPDATE user_points SET points = points + 1")
	db_manager.db.commit()

# Method for sending a message  
def sendMessage(message):
	if message == None:
		return
	print("> " + config.NICK + ": " + message)
	s.send(("PRIVMSG #" + config.CHAN + " :" + message + "\r\n").encode())

# Connecting to Twitch IRC by passing credentials and joining a certain channel 
s = socket.socket()
s.connect((config.HOST, config.PORT))
s.send(("PASS " + config.PASS + "\r\n").encode())
s.send(("NICK " + config.NICK + "\r\n").encode())
s.send(("JOIN #" + config.CHAN + " \r\n").encode())

print("Connected to channel #" + config.CHAN)
db_manager.create_table("`user_points`(user TEXT, points INT)")

while True:
	currentTime = int(round(time.time() * 1000))
	readbuffer = readbuffer + s.recv(1024).decode()
	temp = str.split(readbuffer, "\n")
	readbuffer = temp.pop()

	if currentTime - point_timer >= 3600:
		point_timer += 3600
		add_points()
		print("Added points")


	for line in temp:
		# Checks whether the message is PING because its a method of Twitch to check if you're afk 
		if (line[0] == "PING"):
			s.send(("PONG %s\r\n" % line[1]).encode())
		else:
			# Splits the given string so we can work with it better 
			parts = str.split(line, ":")

			if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
				try:
					# Sets the message variable to the actual message sent 
					message = parts[2][:len(parts[2]) - 1]
				except:
					message = ""
				# Sets the username variable to the actual username 
				usernamesplit = str.split(parts[1], "!")
				username = usernamesplit[0]
				# Only works after twitch is done announcing stuff (MODT = Message of the day) 
				if MOTD:
					#
					#COMMANDS
					#
					try:
						print("> " + username + ": " + message)
					except:
						print("> UTF-8 error")
						continue


					if message.startswith("!"):
						command_args = str.split(message, " ")

						if command_args[0].find('!autism') != -1:
							sendMessage(usercommands.get_autism_level(command_args, username))

						if command_args[0].find("!create_database") != -1:
							if username == config.CHAN != -1 or username == "gasolinebased" != 1:
								sendMessage(usercommands.update_json(db_manager, get_user_json(), get_moderator_json()))
							else:
								sendMessage("Only the streamer can create the database " + config.CHAN)
							#emotes = usercommands.get_message_emotes(message, db_manager)

						if command_args[0].find("!points") != -1:
							sendMessage(usercommands.get_user_points(command_args, username ,db_manager))

						if command_args[0].find("!givepoints") != -1:
							sendMessage(usercommands.give_points(command_args, username, db_manager))

						if command_args[0].find("!roulette") != -1:
							sendMessage(usercommands. roulette(command_args, username, db_manager))

						if command_args[0].find("!playsound") != -1:
							sendMessage(usercommands.play_sound(command_args, username, db_manager))

					#
					#END COMMANDS
					#

				for l in parts:
					if "End of /NAMES list" in l:
						MOTD = True

