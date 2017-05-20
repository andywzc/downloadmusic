
# coding=utf8

import requests
from bs4 import BeautifulSoup

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,en-GB;q=0.2',

'Connection':'keep-alive',
'Cookie':'q_c1=9e2e29e475af4465a34b27c2d03a0cb3|1495169084000|1495169084000; r_cap_id="NzhmMjM1NjY5YjMzNDUwMWJkODFhZDM3MzViOTNhYTg=|1495169101|c02c4b33d15c230deacc81e17ecb154b2f96afbe"; cap_id="MWE1OWQ2ZjE0MTM1NGFjMzk2MTRjNTE2ZDY4ZTdlM2Y=|1495169101|62e40066189fcf13ab14a16c937efe051869f931"; l_cap_id="NzM3OTk3MzhlZmE2NDM3Nzk1MGI4YmVlMGYwMDZjYmE=|1495169101|0c3f4cc01d4c17eead60ae31e6db35c16268d42b"; aliyungf_tc=AQAAAFucVRFeMwIA79AM0qRazTdfI/Cf; _gat=1; _ga=GA1.2.1446388512.1495240468; _gid=GA1.2.660002745.1495240503',

'Referer':'http://daily.zhihu.com/',

'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

url = 'http://daily.zhihu.com/story/9423118'
res = requests.get('http://daily.zhihu.com/',headers)
soup = BeautifulSoup(res.content, 'html.parser')
print soup