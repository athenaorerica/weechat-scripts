__module_name__ = 'mpdnp'
__module_version__ = '1.0'
__module_description__ = 'announces mpd now playing'
__author__ = 'athenaorerica'
__license__ = 'MIT/X11'

import weechat
from mpd import MPDClient
import time
weechat.register(__module_name__, __author__, __module_version__, __license__, __module_description__, "", "")

defaultconfig = {"hostname": "localhost", "port": "6600", "password": ""}

for confname, confval in defaultconfig.items():
  if not weechat.config_get_plugin(confname):
    weechat.config_set_plugin(confname, confval)

def printtobuffer(message):
	weechat.prnt(weechat.current_buffer(), message)

client = MPDClient()

def np(data, buffer, args):
	server = weechat.config_get_plugin('hostname')
	port = weechat.config_get_plugin('port')
	password = weechat.config_get_plugin('password')
	curbuff = weechat.current_buffer()

	client.connect(server, port)
	if password != "":
		client.password(password)

	np = client.currentsong()
	st = client.status()
	title = np.get('title')
	artist = np.get('artist')
	album = np.get('album')
	try:
		elapsed = time.strftime("%M:%S", time.gmtime(int(st.get('time').split(':')[0])))
		duration = time.strftime("%M:%S", time.gmtime(int(st.get('time').split(':')[1])))
	except:
		pass
#	playlistpos = st.get('playlist')
#	playlistlength = st.get('playlistlength')
	bitrate = st.get('bitrate')
	playbackstatus = st.get('state')
#	volume = st.get('volume')
#	date = np.get('date')
#	track = np.get('track')
	if playbackstatus == 'pause':
		if not album: 
			weechat.command(curbuff, '/me np:\00306 %s \017by\00307 %s \017 [\00306%s\017/\00310%s\017] [\00302%s\00313kbps\017] [\00304paused\017] [\00309mpd %s\017]' % (title, artist, elapsed, duration, bitrate, client.mpd_version))
		if album: 
			weechat.command(curbuff, '/me np:\00306 %s \017by\00307 %s\017 from\00310 %s\017 [\00306%s\017/\00310%s\017] [\00302%s\00313kbps\017] [\00304paused\017] [\00309mpd %s\017]' % (title, artist, album, elapsed, duration, bitrate, client.mpd_version))
	elif playbackstatus == 'play':
		if not album: 
			weechat.command(curbuff, '/me np:\00306 %s \017by\00307 %s \017 [\00306%s\017/\00310%s\017] [\00302%s\00313kbps\017] [\00309mpd %s\017]' % (title, artist, elapsed, duration, bitrate, client.mpd_version))
		if album: 
			weechat.command(curbuff, '/me np:\00306 %s \017by\00307 %s\017 from\00310 %s\017 [\00306%s\017/\00310%s\017] [\00302%s\00313kbps\017] [\00309mpd %s\017]' % (title, artist, album, elapsed, duration, bitrate, client.mpd_version))
	elif playbackstatus == 'stop':
		weechat.command(curbuff, '/me np: [\00304playback stopped\017] [\00309mpd %s\017]' % client.mpd_version)
	client.close()
	client.disconnect()
	return weechat.WEECHAT_RC_OK

weechat.hook_command("np", "shows now playing on mpd", "", "", "", "np", "")