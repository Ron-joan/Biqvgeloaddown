import re
import requests
from bs4 import BeautifulSoup
import time

def getHTMLText(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, timeout=50,headers = kv)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return getHTMLText(url)

def getonepage(page_url,path):
    f = open(path,'a',encoding="utf-8")
    onetext = getHTMLText(page_url)
    soup = BeautifulSoup(onetext, "html.parser")
    title = soup.find_all('h1')[0]
    t = '\n' + title.string + '\n'
    f.write(t)
    for line in soup.find_all(re.compile('br')):
        try :
            if '亲,点击进去' not in line.previous_sibling.string:
                f.write(line.previous_sibling.string)
            else:
                break
        except:
            continue
    #time.sleep(1.2)
    f.close()
    return ""

def getallpage(catalogue_url,path):
    text = getHTMLText(catalogue_url)
    soup = BeautifulSoup(text, features = "html.parser")
    count = 1
    title = soup.find_all('h1')[0]
    path = path + title.string + '.txt'
    for pages in soup.find_all('dd'):
        all = len(soup.find_all('dd'))
        for page in pages.children:
            page_url = catalogue_url[:-10] + page.attrs['href']
            getonepage(page_url,path)
            print('当前进度为{:.2f}%'.format(count*100/all))
            count = count + 1
    return ""

def main():
    start_url = 'http://www.xbiquge.la/29/29911/'
    path = 'D:/novel/'
    getallpage(start_url,path)
main()