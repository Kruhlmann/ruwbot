#duel_test
import sqlite3
import config

from random import randint

db = sqlite3.connect("db/duels.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS active_duels (duelist1 TEXT, duelist2 TEXT, amount INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS requested_duels (duelist1 TEXT, duelist2 TEXT, amount INT)")
db.commit()

#'duelist1' has requested a duel for 'amount' against 'duelist2'
def request_duel(duelist1, duelist2, amount, db_manager):

	cursor.execute("SELECT * FROM requested_duels WHERE duelist1=\'" + duelist1 + "\' AND duelist2=\'" + duelist2 + "\'")
	if cursor.fetchone() is not None:
		return (duelist1 + " you have already requested a duel with " + duelist2 + " (" + str(amount) + " points)")
	else:
		cursor.execute("SELECT * FROM requested_duels WHERE duelist2=\'" + duelist2 + "\'")
		if cursor.fetchone():
			return (duelist2 + " already has a duel pending!")
		else:
			return ("A duel with " + duelist2 + " has been requested for " + str(amount) + " points")
			cursor.execute("INSERT INTO requested_duels VALUES (\'" + duelist1 + "\', \'" + duelist2 + "\', " + str(amount) + ")")
			db.commit()

#'duelist2' has accepted the duel
def accept_duel(duelist1, db_manager):
	points = db_manager.get_user_points(duelist1)

	cursor.execute("SELECT * FROM requested_duels WHERE duelist2=\'" + duelist1 + "\'")
	data = cursor.fetchone()
	if data is not None:
		opponent = data[0]
		wager = data[2]
		if wage > points:
			return (duelist1 + " you only have " + points + " points and can't accept this duel for " + wager + " points")
		if randint(0, 1) == 1:
			if randint(0, 100) <= 50:
				return (duelist1 + " just won " + str(wager) + " from " + opponent)
			else:
				return (duelist1 + " just lost " + str(wager) + " against " + opponent)
			cursor.execute("DELETE FROM requested_duels WHERE duelist2=\'" + duelist1 + "\'")
		else:
			return ("The duel between " + duelist1 + " and " + opponent + " for " + str(wager) + " points has been declined")
			cursor.execute("DELETE FROM requested_duels WHERE duelist2=\'" + duelist1 + "\'")
		db.commit()
	else:
		return (duelist1 + " you currently have no duels pending")