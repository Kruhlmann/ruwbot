#duel_test
import sqlite3

from random import randint

db = sqlite3.connect("duels.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS active_duels (duelist1 TEXT, duelist2 TEXT, amount INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS requested_duels (duelist1 TEXT, duelist2 TEXT, amount INT)")
db.commit()

#'duelist1' has requested a duel for 'amount' against 'duelist2'
def request_duel(duelist1, duelist2, amount):

    cursor.execute("SELECT * FROM requested_duels WHERE duelist1=\'" + duelist1 + "\' AND duelist2=\'" + duelist2 + "\'")
    if cursor.fetchone() is not None:
    	print(duelist1 + " you have already requested a duel with " + duelist2 + " (" + str(amount) + " points)")
    else:
	    cursor.execute("SELECT * FROM requested_duels WHERE duelist2=\'" + duelist2 + "\'")
	    if cursor.fetchone():
	    	print(duelist2 + " already has a duel pending!")
    	else:
    		print("A duel with " + duelist2 + " has been requested for " + str(amount) + " points")
    		cursor.execute("INSERT INTO requested_duels VALUES (\'" + duelist1 + "\', \'" + duelist2 + "\', " + str(amount) + ")")
    		db.commit()
#'duelist2' has accepted the duel
def accept_duel():

    cursor.execute("SELECT * FROM requested_duels WHERE duelist2=\'" + duelist1 + "\'")
    data = cursor.fetchone()
    if data is not None:
	    opponent = data[0]
	    wager = data[2]
	    if randint(0, 1) == 1:
		    if randint(0, 100) <= 50:
			    print(duelist1 + " just won " + str(wager) + " from " + opponent)
		    else:
			    print(duelist1 + " just lost " + str(wager) + " against " + opponent)
		    cursor.execute("DELETE FROM requested_duels WHERE duelist2=\'" + duelist1 + 
        else:
		    print("The duel between " + duelist1 + " and " + opponent + " for " + str(wager) + " points has been declined")
		    cursor.execute("DELETE FROM requested_duels WHERE duelist2=\'" + duelist1 + "\'")
        db.commit()
    else:
	    print(duelist1 + " you currently have no duels pending")

request_duels("gasolinebased", "ruwin", 50)
#accept_duel("ruwin")
