#usercommands.py
import winsound
import config
import duel

from random import randint

def play_sound(command_args, username, db_manager):
	if len(command_args) < 2:
		sounds = ""
		for sound in config.sounds:
			sounds += sound + ", "
		return("The list of sounds are currently: " + sounds)
	else:
		points = db_manager.get_user_points(username)

		if points >= config.SOUND_COST:
			if command_args[1] in config.sounds:
				db_manager.update_user(username, points - config.SOUND_COST)
				print("Playing sound " + "sound/" + command_args[1] + ".wav")
				winsound.PlaySound("sound/" + command_args[1] + ".wav", winsound.SND_FILENAME)
				return(None)
			else:
				return("The sound " + command_args[1] +  " is not in the library! You have not been charged any points.")
		else:
			return("Sorry " + username + " you need " + str(config.SOUND_COST) + " points to play a sound! (You have " + points + ")")

def play_premium_sound(command_args, username, db_manager):
	if len(command_args) < 2:
		sounds = ""
		for sound in config.premium_sounds:
			sounds += sound + ", "
		return("The list of premium sounds are currently: " + sounds)
	else:
		points = db_manager.get_user_points(username)

		if points >= config.PREMIUM_SOUND_COST:
			if command_args[1] in config.premium_sounds:
				db_manager.update_user(username, points - config.PREMIUM_SOUND_COST)
				print("Playing premium sound " + "sound/" + command_args[1] + ".wav")
				winsound.PlaySound("sound/" + command_args[1] + ".wav", winsound.SND_FILENAME)
				return(None)
			else:
				return("The premium sound " + command_args[1] +  " is not in the library! You have not been charged any points.")
		else:
			return("Sorry " + username + " you need " + str(config.PREMIUM_SOUND_COST) + " points to play a premium sound! (You have " + points + ")")

def play_sound_combo(command_args, username, db_manager):
	if len(command_args) < 2:
		sounds = ""
		for sound in config.sound_combos:
			combo_n = str.split(sound, ";")[0] + " "
			sounds += combo_n
		return("The list of sounds combos are currently: " + sounds)
	else:
		points = db_manager.get_user_points(username)

		if points >= config.PREMIUM_SOUND_COST:
			found_combo = 0
			combo_name = ""

			for combo in config.sound_combos:
				combo = str.split(combo, ";")
				combo_name = combo[0]
				if combo_name == command_args[1]:
					found_combo = 1
					break

			if found_combo == 1:
				for combo in config.sound_combos:
					combo = str.split(combo, ";")
					combo_name = combo[0]

					if combo_name == command_args[1]:
						db_manager.update_user(username, points - config.SOUND_COMBO_COST)
						print("Playing sound combo " + combo_name)
						winsound.PlaySound("sound/" + combo[1] + ".wav", winsound.SND_FILENAME)
						winsound.PlaySound("sound/" + combo[2] + ".wav", winsound.SND_FILENAME)
						return(None)
			else:
				return("The sound combo " + command_args[1] +  " is not in the library! You have not been charged any points.")
		else:
			return("Sorry " + username + " you need " + str(config.SOUND_COMBO_COST) + " points to play a premium sound! (You have " + points + ")")

def get_autism_level(command_args, username):
	sender = username
	if len(command_args) > 1:
		sender = command_args[1]
	randLevel = randint(0,100)
	if str.lower(sender).find("tkeey") != -1:
		randLevel = randint(80,100)
	emote = ""
	if randLevel <= 30:
		emote = "FeelsGoodMan"
	elif randLevel <= 75:
		emote = "FeelsBadMan"
	else:
		emote = "EleGiggle"
	return(sender + " is " + str(randLevel) + "%" + " autistic " + emote)

def update_json(db_manager, chatters, mods):
	print("Fetching JSON for channel " + config.CHAN)

	if chatters != False:
		try:
			for chatter in chatteis:
				q = db_manager.query("SELECT * FROM user_points WHERE user = \'" + chatter + "\'")
				if q.fetchone() == None:
					db_manager.create_user(chatter)
					print("Creating user " + chatter)
				else:
					print("Chatter " + chatter + " already exists in the database")
		except:
			return "An error occured while fetching user JSON from the twitch API. Try again"

	if mods != False:
		try:
			for mod in mods:
				q = db_manager.query("SELECT * FROM user_points WHERE user = \'" + mod + "\'")
				if q.fetchone() == None:
					db_manager.create_user(mod)
					print("Creating user " + mod)
				else:
					print("Mod " + mod + " already exists in the database")
		except:
			return "An error occured while fetching mod JSON from the twitch API. Try again"

def get_user_points(command_args, username, db_manager):
	sender = username
	if len(command_args) > 1:
		sender = command_args[1]
	user_points = db_manager.get_user_points(sender)
	if user_points == None:
		return ("The user " + sender + " was not found. Creating the user in the database now")
		db_manager.create_user(sender)
	else:
		return ("User " + sender + " has " + str(user_points) + " points")

def give_points(command_args, username, db_manager):
	if username.find("gasolinebased") != -1:
		points = 100
		user = "gasolinebased"
		if len(command_args) > 1:
			points = isInt(command_args[1])
		if len(command_args) > 2:
			user = command_args[2]
		user_points = db_manager.get_user_points(username)

		if points == False:
			return (command_args[1] + " is not a number")
		if user_points == None:
			return ("The user " + user + " was not found. Creating the user in the database now")
			db_manager.create_user(user, points)
		else:
			db_manager.update_user(user, user_points + points)
			return ("User " + user + " was given " + str(points) + " points")
	else:
		return ("Nice try " + username + " 4Head")

def roulette(command_args, username, db_manager):
	if len(command_args) < 2:
		return (username + " you need to specify an amount to roll [!roulette 37]")
	else:
		gamble = int(command_args[1])
		user_points = db_manager.get_user_points(username)
		if user_points == None:
			return (username + " you dont exist in the database. creating you now")
			db_manager.create_user(username)
		else:
			if user_points < gamble:
				return ("Sorry " + username + " you only have " + str(user_points) + " points")
			else:
				roll = randint(5, 100)
				if roll < 50:
					return (username + " just won " + str(gamble) + " points in the roulette FeelsGoodMan")
					db_manager.update_user(username, user_points + gamble)
				else:
					return (username + " just lost " + str(gamble) + " points in the roulette FeelsBadMan")
					db_manager.update_user(username, user_points - gamble)

def get_message_emotes(message, db_manager):
	parts = str.split(message, " ")
	db_manager.update_emote_db()
	for part in parts:
		print(part)

def get_developer_info():
	return ("This bot has been programmed for twitch.tv/ruwin by Andreas Kruhlmann. The source code is avaliable on github (https://github.com/kruhlmann).")

def isInt(s):
    try: 
        return int(s)
    except ValueError:
        return False