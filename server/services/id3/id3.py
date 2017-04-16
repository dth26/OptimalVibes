import eyed3
from globals import Globals

class ID3TagEditInterface:

	def editTag(self, artist, song, full_filename):
		song_path = '{}/{}'.format(Globals.DOWNLOAD_PATH, full_filename)
		#song_path = song_path.replace(' ','\\ ')
		print 'song path: ',song_path
		audiofile = eyed3.load(song_path)
		audiofile.initTag()
		audiofile.tag.artist = artist.decode('utf-8')
		audiofile.tag.title = song.decode('utf-8')


		audiofile.tag.save()