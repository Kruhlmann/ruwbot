#bot.py
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import _thread
import time
import random
import sys
import re
import string
import json
import sqlite3

from tkinter import *
from tkinter.ttk import *

import duel
import config
import usercommands

from db_manager import Db_Manager

try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

def bot_thread():
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

	def reset_points():
		db_manager.query("UPDATE user_points SET points = 0")

	# Method for sending a message  
	def sendMessage(message):
		if message == None:
			return
		print("> " + config.NICK + ": " + message)
		s.send(("PRIVMSG #" + config.CHAN + " :" + message + "\r\n").encode())

	readbuffer = ""
	MOTD = False
	point_timer = int(round(time.time() * 1000))

	# Connecting to Twitch IRC by passing credentials and joining a certain channel 
	s = socket.socket()
	s.connect((config.HOST, config.PORT))
	s.send(("PASS " + config.PASS + "\r\n").encode())
	s.send(("NICK " + config.NICK + "\r\n").encode())
	s.send(("JOIN #" + config.CHAN + " \r\n").encode())
	db_manager = Db_Manager(config.CHAN)

	print("Connected to channel #" + config.CHAN)
	db_manager.create_table("`user_points`(user TEXT, points INT)")
	db_manager.update_emote_db()
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

						#Create user
						user_points = db_manager.get_user_points(username)
						if user_points == 0 or user_points == None:
							db_manager.create_user(username)


						if message.startswith("!"):
							command_args = str.split(message, " ")

							if command_args[0] == '!logoff':
									if username == "gasolinebased" or username == config.CHAN:
										exit()

							if command_args[0] == '!autism':
								sendMessage(usercommands.get_autism_level(command_args, username))

							if command_args[0] == "!create_database":
								if username == config.CHAN != -1 or username == "gasolinebased" != 1:
									sendMessage(usercommands.update_json(db_manager, get_user_json(), get_moderator_json()))
								else:
									sendMessage("Only the streamer can create the database " + config.CHAN)
								#emotes = usercommands.get_message_emotes(message, db_manager)

							if command_args[0] == "!points":
								sendMessage(usercommands.get_user_points(command_args, username ,db_manager))

							if command_args[0] == "!givepoints":
								sendMessage(usercommands.give_points(command_args, username, db_manager))

							if command_args[0] == "!roulette":
								sendMessage(usercommands. roulette(command_args, username, db_manager))

							if command_args[0] == "!playsound":
								sendMessage(usercommands.play_sound(command_args, username, db_manager))

							if command_args[0] == "!premiumsound":
								sendMessage(usercommands.play_premium_sound(command_args, username, db_manager))

							if command_args[0] == "!updateemotes":
								db_manager.update_emote_db()
								sendMessage("Emote database has been updated! 4Head")

							if command_args[0] == "!playcombo":
								sendMessage(usercommands.play_sound_combo(command_args, username, db_manager))
							if command_args[0] == "!duel":
								if(len(command_args) < 3):
									sendMessage(username + ", you need to use the syntax: !duel username amount")
								else:
									sendMessage(duel.request_duel(username, command_args[1], command_args[2], db_manager))

							#if command_args[0] == "!accept":
							#	sendMessage(duel.accept_duel(username, db_manager))

							if command_args[0] == "!resetdb":
								if username == "ruwin" or username == "gasolinebased":
									reset_points()
									sendMessage("Points have been reset to 0 for all users by " + username)
								else:
									sendMessage("Sorry " + username + ", you don't have permission to execute that command FeelsBadMan")


						#
						#END COMMANDS
						#

					for l in parts:
						if "End of /NAMES list" in l:
							MOTD = True

#when ran
global version
version = "0.4"
global screen_emotes

bot_thread_p = threading.Thread(target=bot_thread)
bot_thread_p.start()

