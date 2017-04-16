from flask import request, jsonify
import subprocess
import sys
import time
import glob
import os
#sys.path.append('/Users/danielhui/Documents/apps/OptimalVibes/server/')
sys.path.append('/Users/danielhui/Documents/apps/OptimalVibes/server')
from globals import Globals
from status import Status
from models.songs import SongModel

class YoutubeDLInterface(object):



	def __init__(self):
		self.songModel = SongModel()


	#
	#
	#	Params
	#		=> URL : spotify uri, youtube playlist url, youtube song url
	#
	#	Returns
	#		=> {
	#			status : {
	#				'status' : boolean,
	#				'description' : string
	#			},
	#			artist: string,
	#			song: string,
	#			id: int
	#		}
	#
	#
	def parseRequest(self, URL, artist=None, song=None):
		"""Figure out what kind of download option the user wants"""

		statusObject = Status()
		ytdl_cmd_args = [] 		# append cmd arguments to this
		

		self.download(URL, ytdl_cmd_args, statusObject)

		#print statusObject.toDict()

		return statusObject




	#
	#	Params
	#		=> URL : spotify uri, youtube playlist url, youtube song url
	#		=> ytdl_cmd_args : optional youtube-dl command line arguments
	#	Returns
	#		=> 	statusObject : only return if none is provided in function call
	#		
	#
	#
	#####################
	#
	#
	#	ISSUE fix duplicate track error
	#		youtube-dl error occurs when you download a track with a filename that already exists
	#
	#####################
	def download(self, URL, filename=None, pid=None, fid=None, ytdl_cmd_args=[]):
		"""Do the actual downloading"""

		ret_vals = dict()

		#args = ['youtube-dl','--audio-format','mp3'] + ytdl_cmd_args + ['-q',URL]
#		proc_v = subprocess.call('youtube-dl', ytdl_cmd_opts, URL)
		statusObject = Status()


		if filename is None or filename is '':
			print 'filename is None =============='
			cmd = '{} --verbose --audio-quality 0 --extract-audio --audio-format mp3 {} -q {} -o "{}/%(title)s.%(ext)s";'.format(Globals.YTDL_BINARY_PATH, ''.join(ytdl_cmd_args), URL, Globals.DOWNLOAD_PATH)
		else:
			print 'filename is not None ==============='
			cmd = '{} --verbose  --audio-quality 0 --extract-audio --audio-format mp3 {} -q {} -o "{}/{}.%(ext)s";'.format(Globals.YTDL_BINARY_PATH, ''.join(ytdl_cmd_args), URL, Globals.DOWNLOAD_PATH, filename)

		print 'download:s'
		print cmd

		try:
			cmd_req = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
			statusObject.setSuccess(True)

			if fid is None:
				fid = int(time.time())

			list_of_uploads = glob.glob(Globals.DOWNLOAD_PATH + '/*') # * means all if need specific format then *.csv
			latest_upload = max(list_of_uploads, key=os.path.getctime)
			latest_upload = latest_upload.split('/')[-1][0:-4]	
			ret_vals['filename'] = latest_upload		# filename of song

			self.songModel.addSong(fid=fid, filename=latest_upload, pid=pid)

		except Exception as inst:
			statusObject = Status()
		#	self.dump(statusObject)
			print 'Exception: '
			print inst
			statusObject.setSuccess(False)
			statusObject.setDescription(inst)
			ret_vals['filename'] = None		# filename of song

	
		
		ret_vals['fid'] = fid
		ret_vals['status'] = statusObject.toDict()



		return ret_vals




	def formatSongFilename(self, artist, song, filename=None):

		if filename is None:
			filename = '{} - {}'.format(artist, song)

		filename = filename.replace('$','S')		# these characters cannot be included in a filename
		return filename





	def dump(self, obj):
		for attr in dir(obj):
			if hasattr( obj, attr ):
				print( "obj.%s = %s" % (attr, getattr(obj, attr)))





	def serveDownload(self):
		pass


