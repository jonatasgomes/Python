from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_tag(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    except URLError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), 'lxml')
        tag = bs.find_all(id='text')
    except AttributeError as e:
        return None
    return tag

tag = get_tag('http://www.pythonscraping.com/pages/warandpeace.html')
if tag is None:
    print('Not found')
else:
    print(len(tag))
    # for t in tag:
        # print(t, t.text)
