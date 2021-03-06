import bs4
import requests
import os


def song_parser():
    requested = requests.get("http://openings.moe/list/")
    souphtml = bs4.BeautifulSoup(requested.text)
    results = []
    for item in souphtml.select(".series a"):
        hrefitem = item.get("href")
        hrefitem = hrefitem.split("=")
        results.append(hrefitem[1])
    return results


def vid_downloader(songlist):
    try:
        os.mkdir("Downloaded Songs")
    except (FileExistsError):
        print("Folder is already created. Skipping...")
    for song in songlist:
        # Formatting the URL and saving song to variable
        songurl = ("http://openings.moe/video/" + song + ".webm")
        print("Downloading %s..." % (song))
        # Saving video to file
        if os.path.isfile(os.path.join("Downloaded Songs", os.path.basename(songurl))) is True:
            print(song + " already exists. Skipping...")
        else:
            songvar = requests.get(songurl)
            songvar.raise_for_status()
            songfile = open(os.path.join("Downloaded Songs", os.path.basename(songurl)), "wb")
            for chunk in songvar.iter_content(100000):
                songfile.write(chunk)
            songfile.close
    print("Done!")


vid_downloader(song_parser())
