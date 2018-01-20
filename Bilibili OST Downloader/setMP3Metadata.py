from mutagen.easyid3 import EasyID3
import os
import re

flist = [i for i in os.listdir(".") if os.path.splitext(i)[1] == ".mp3"]

for i in flist:
    audio = EasyID3(i)
    audio["title"] = os.path.splitext(i)[0]
    audio["album"] = "ALBUM"
    audio["artist"] = "ARTIST"
    audio["composer"] = "COMPOSER"
    audio["genre"] = "Game - OST"
    audio["tracknumber"] = re.findall("\d+", os.path.splitext(i)[0])[0]
    audio.save()
