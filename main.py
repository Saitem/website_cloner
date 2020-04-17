from urllib.request import Request, urlopen, urljoin, urlretrieve
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

url = 'Website which you want clone'

def getPage(url):
    try:
        req = Request(url)
        return urlopen(req).read().decode(encoding = 'utf-8', errors = 'ignore')
    except HTTPError as e:
        return None
    except URLError as e:
        return None

def getSoup(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except AttributeError as e:
        return None

def getImageLocations(page):
    img_regex = re.compile('<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
    return img_regex.findall(page)

def displayImageLocations(images):
    arr = []
    for src in images:
        arr.append(urljoin(target_url, src))
    return arr

def extractLinks(page):
    arr = []
    links = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE).findall(page)
    for link in links: 
        arr.append(urljoin(target_url, link))
    
    return arr

def filterLinks(links):
    arr = []
    for link in links:
        if url in link and link not in arr:
            arr.append(link)

    return arr

def getCssLocations(page):
    arr = []
    soup = getSoup(page)
    css_name_list = soup.findAll('link', { 'rel': 'stylesheet' })

    for i in css_name_list:
        arr.append(i.get('href'))
        
    return arr 

def getJsLocations(page): 
    arr = []
    soup = getSoup(page)
    js_name_list = soup.findAll('script')

    for i in js_name_list:
        i = i.get('src')
        if str(i)[0] == '/':
            arr.append(i)

    return arr

def downloadJs(page):
    js_name_list = getJsLocations(page)

    for i in js_name_list:
        link = urljoin(target_url, i)
        urlretrieve(link, str(i[1:]))

def downloadCss(page):
    css_name_list = getCssLocations(page)

    for i in css_name_list:
        link = urljoin(target_url, i)
        urlretrieve(link, str(i[1:]))

def downloadPages(links):
    for link in links:

        bn = '/'.join(link.split('/')[-1:])
        path = '/'.join(link.split('/')[3:-1])

        name = os.path.basename(bn)

        if len(name) < 6:
            name = 'index.html'
        elif '.html' not in name:
            name = name + '.html'
        
        page = getPage(link)
        
        with open(os.path.join(path, name), 'w') as file:
            try:
                soup = getSoup(page)
                file.write(str(soup))
            except:
                pass
     
def downloadImages(urls):
    for url in urls:
        path = '/'.join(url.split('/')[3:])
        urlretrieve(url, str(path))
   
def createFolders(links):
    arr = []
    link_loc = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE).findall(page)
    img_loc = getImageLocations(page)
    css_loc = getCssLocations(page)
    js_loc = getJsLocations(page)
    
    final_loc = link_loc + img_loc + css_loc + js_loc
  
    for link in final_loc:
        if link not in arr and len(link) != 1 and link.split('/')[0] == '' and link != '':
            try:
                os.makedirs('/'.join(link.split('/')[1:-1]))
            except OSError:
                pass
  
def init():
    getImgLoc = getImageLocations(page)
    disp = displayImageLocations(getImgLoc)
    links = extractLinks(page)
    filterLink = filterLinks(links)
    
    createFolders(page)
    downloadImages(disp)
    downloadCss(page)
    downloadPages(filterLink)
    downloadJs(page)

if __name__ == '__main__':
    target_url = url
    page = getPage(target_url)
    init()
   
    