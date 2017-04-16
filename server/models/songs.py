from app import app
from flaskext.mysql import MySQL
import peewee
from peewee import *
import mysql.connector  


# conn = mysql.connect()
# cursor =conn.cursor()

# cursor.execute("SELECT * from User")
# data = cursor.fetchone()


class SongModel(object):


	#############################
	# connect with MYSQL        #
	#############################
	def __init__(self):	
		mysql = MySQL()
		mysql.init_app(app)
		self.conn = mysql.connect()
		#self.cursor = self.conn.cursor()

		db = mysql.connector.connect(user='root', 
								password='@zxcvbnm3',
                              	host='127.0.0.1',
                             	 database='optimalvibes')

	
		self.cursor = db.cursor()
		   # cursor.execute("""
		   #    select 3 from your_table
		   # """)
		   # result = cursor.fetchall()
		   # print result


	def getSong(self, filename):
		query = 'SELECT * FROM songs WHERE filename={};'.format(filename)
		self.cursor.execute(query)
		data = self.cursor.fetch()

		print 'MYSQL =======> ', data

		self.conn.close()

		return data

	def addSong(self, fid, filename, pid=None, name=None, artist=None):

		if pid == '':
			pid = 'None' 

		query = 'INSERT INTO `songs` (`id`,`filename`,`playlistID`) VALUES ("{}","{}","{}");'.format(fid, filename, pid)

		self.cursor.execute("""SELECT * FROM `songs`""")
		result = cursor.fetchone()
		print result
		print 'QUERY =====> ' ,query
		self.cursor.execute(query)
		# data = self.cursor.fetch()

		# print 'MYSQL =======> ', data

		self.conn.close()

		return 1







db = MySQLDatabase('jonhydb', user='john',passwd='megajonhy')

class Book(peewee.Model):
    author = peewee.CharField()
    title = peewee.TextField()

    class Meta:
        database = db

Book.create_table()
book = Book(author="me", title='Peewee is cool')
book.save()
for book in Book.filter(author="me"):
    print book.title