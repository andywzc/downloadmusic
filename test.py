
import requests
from bs4 import BeautifulSoup
import threading
import Queue


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
        url = site + str(vol)
        # print url

        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        # print soup

        vol = int(soup.find('span', attrs={'class' : 'vol-number'}).text)

        title = soup.find('span', attrs={'class' : 'vol-title'}).text
        track_names = soup.find_all('a', attrs={'class' : 'trackname'})
        count = len(track_names)
        # print vol

        tracks = []


        for track in track_names:
            # print track.text
            # print len(track.text)
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
            # print vol
            self.spider(vol)
            print self.queue.get()




class DownLoad:

    def __init__(self,data):
        self.data = data

    def download(self):
        vol = self.data['vol']
        for track in self.data['tracks']:
            a = track['id']
            b = track['name']
            musicurl = site_music % (vol,a)
            print musicurl
            local_file = 'I:/music/%s.%s.mp3' % (a, b)


            req = requests.get(musicurl,headers)
            with open(local_file, 'wb') as f:
                f.write(req.content)
                print req.content
                f.close()
            print 'done.\\n'

vols=[3,4,5,6]
ms = MusicSpider(site, vols,queue=Queue.Queue())

for i in vols:
    ms.start()

    md = DownLoad(ms.queue.get())
    md.download()