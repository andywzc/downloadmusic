# coding:utf-8

import os
import requests
from bs4 import BeautifulSoup
import random
from faker import Factory
import Queue
import threading

#http://mp3-cdn2.luoo.net/low/luoo/radio916/03.mp3

fake = Factory.create()
site = 'http://www.luoo.net/music/'
site_music = 'http://mp3-cdn2.luoo.net/low/luoo/radio%s/%s.mp3'

headers = {
    'Accept-Encoding':'identity;q=1, *;q=0',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,en-GB;q=0.2',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

class MusicSpider(threading.Thread):
    def __init__(self, url, vols,queue=None):
        threading.Thread.__init__(self)
        self.url = url
        self.vols = vols
        self.vol = 1
        self.queue = queue

    def spider(self, vol):
        url = site + vol
        print url

        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        print soup

        vol = int(soup.find('span', attrs={'class' : 'vol-number'}).text)

        title = soup.find('span', attrs={'class' : 'vol-title'}).text
        track_names = soup.find_all('a', attrs={'class' : 'trackname'})
        count = len(track_names)
        print vol

        tracks = []


        for track in track_names:
            print track.text
            print len(track.text)
            _id = str(int(track.text[:2])) if (int(vol) < 12) else track.text[:2]
            _name = track.text[4:]

            tracks.append({'id' : _id, 'name' : _name})

            data = {
                'vol' : vol,
                'tracks' : tracks
            }

            self.queue.put(data)


    def run(self):


        for vol in self.vols:
            print vol
            self.spider(vol)


class MyDownload(threading.Thread):
    def __init__(self, url, vol, queue,disk):
        threading.Thread.__init__(self)
        self.vol = vol
        self.queue = queue
        self.url = url
        self.disk = disk

    def run(self):
        while True:
            if self.queue.qsize() <= 0:
                pass
            else:
                data = self.queue.get()
                self.download(data)

    def download(self, data):
        for track in data['tracks']:
            music_url = self.url % (data['vol'], track['tracks'])

            print music_url
            local_file_dict = '%s/%s' % (self.disk, data['vol'])
            if not os.path.exists(local_file_dict):
                os.makedirs(local_file_dict)

            local_file = '%s/%s.%s.mp3' % (local_file_dict, track['id'], track['name'])
            if not os.path.isfile(local_file):
                print 'downloading: ' + track['name']
                res = requests.get(music_url, headers=headers)
                with open(local_file, 'wb') as f:
                    f.write(res.content)
                    f.close()
                print 'done.\\n'
            else:
                print 'break: ' + track['name']




ms = MusicSpider(site,vols=['1'],queue=Queue.Queue())
ms.setDaemon(True)
ms.start()
count =5
for i in range (count):
    md = MyDownload(site_music,0,ms.queue,'F:/music')
    md.setDaemon(True)
    md.start()















