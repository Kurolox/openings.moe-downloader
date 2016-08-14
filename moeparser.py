import bs4
import requests
import re
import os


def song_parser():
    requested = requests.get("http://openings.moe/list/")
    souphtml = bs4.BeautifulSoup(requested.text)
    htmlist = souphtml.select("a[href]")
    # Since I can't make it cleaner I'll manually remove the exceptions
    for exception in range(4):
        htmlist.pop(0)
    # I'm too dumb to use bs4 correctly, so I'm just gonna regex the results.
    regexedresults = []
    pattern = re.compile(r'(video=)(.*)(")')
    for item in htmlist:
        mo = pattern.search(str(item))
        regexedresults.append(mo.group(2))
    return regexedresults


def vid_downloader(songlist):
    try:
        os.mkdir("Downloaded Songs")
    except (FileExistsError):
        print("Folder is already created. Skipping...")
    for song in songlist:
        # Formatting the URL and saving song to variable
        songurl = ("http://openings.moe/video/" + song + ".webm")
        print("Downloading %s..." % (song))
        songvar = requests.get(songurl)
        songvar.raise_for_status()
        # Saving video to file
        songfile = open(os.path.join("Downloaded Songs", os.path.basename(songurl)), "wb")
        for chunk in songvar.iter_content(100000):
            songfile.write(chunk)
        songfile.close
    print("Done!")


vid_downloader(song_parser())
