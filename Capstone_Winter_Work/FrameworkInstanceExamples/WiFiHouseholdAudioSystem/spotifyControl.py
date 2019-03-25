import subprocess, spotipy, random
from spotipy import util

class Music():

	username = "bradyjibanez"
	scopes = "user-modify-playback-state"
	client_id = "1880307e33e34d32b068cfb792657794"
	client_secret = "a3f3ab263982426aaa109da584df3b83"
	redirect_uri = "http://localhost:8888"
	token = util.prompt_for_user_token(username=username, scope=scopes, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
	service = spotipy.Spotify(auth=token)

	def chooseMusic(self, castId):
		service = spotipy.Spotify(auth=Music.token)
		random_song = str(random.randint(1, 110))
		context_uri_playlist = "{\"context_uri\":\"spotify:user:daniel.ibanez-ca:playlist:60kbkHcSmDeLfkwWf6Voc8\",\"offset\":{\"position\": " + random_song + "}}"
		context_uri_artist = "{\"context_uri\":\"spotify:artist:36QJpDe2go2KgaRleHCDTp\",\"offset\":{\"position\": " + random_song + "}}"
		context_uri_album = "{\"context_uri\":\"spotify:track:4FhOjGTVa4oAi4UMCZ9dPc\"}"

		tunes = subprocess.call(["curl", "-X", "PUT",
		"https://api.spotify.com/v1/me/player/play?device_id=" + str(castId),
		"--data", str(context_uri_playlist),
		"-H", "Accept: application/json", "-H", "Content-Type: application/json",
		"-H", "Authorization: Bearer " + str(Music.token)])

		return tunes

#test = Music()
#test.chooseMusic()




