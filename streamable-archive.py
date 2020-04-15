'''
	streamable-archive.py
	https://github.com/doge
	
	usage:
		launch the program and login with your username and password ( 2fa not supported ). 
		then it will download all the videos it finds on your streamable account and save 
		the outputs to a folder named videos where the program is located.

'''

import requests
import time
from getpass import getpass
from os import system
from pathlib import Path

# set window title
system("title streamable archiver")

page_num = 1
video_count = 0

print("streamable archiver")
print("https://github.com/doge/streamable-archiver\n")

username = input("username: ")
password = getpass("password: ")

with requests.Session() as s:
    # login to streamable and set session cookie
    response = s.post("https://ajax.streamable.com/check", json=dict(username=username, password=password))
    s.cookies['cookie'] = response.headers['set-cookie']

    # check if there's videos on the account
    data = s.get("https://ajax.streamable.com/videos?sort=date_added&count=100&page=%s" % page_num).json()
    if data['total'] == 0:
        print("[*] there are 0 videos found in the account supplied.")
        print("[*] the program will now exit...")
        time.sleep(5)
    else:
        # make the videos directory
        Path("./videos").mkdir(parents=True, exist_ok=True)
        while True:
            print("[*] %s videos found\n" % data['total'])
            for video in data['videos']:
                url = s.get("https:" + video['files']['mp4']['url'])
                file_id = video['file_id']
                print("[%s][%s.mp4] downloading..." % (video_count + 1, file_id))
                with open('./videos/' + file_id + '.mp4', 'wb') as file:
                    try:
                        file.write(url.content)
                        print("[%s][%s.mp4] success!\n" % (video_count + 1, file_id))
                    except:
                        print("[%s][%s.mp4] failed." % (video_count + 1, file_id))
                video_count += 1

            if data['total'] > video_count:
                # if we find out there is another page, go to the next and refresh the data
                page_num += 1
                data = s.get("https://ajax.streamable.com/videos?sort=date_added&count=100&page=%s" % page_num).json()
            elif data['total'] == video_count:
                break
