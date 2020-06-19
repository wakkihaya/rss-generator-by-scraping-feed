from bs4 import BeautifulSoup
import urllib.request
from feedgen.feed import FeedGenerator
from urllib.parse import urlparse
from urllib.error import URLError

# 指定したID or class下の、aタグhrefとtextをとる


def scrape_html(newsFeedURL, domElement, isDomId):
    try:
        data = urllib.request.urlopen(newsFeedURL)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:
        soup = BeautifulSoup(data, 'lxml')
        title = soup.title.getText()
        baseURL = '{uri.scheme}://{uri.netloc}'.format(
            uri=urlparse(newsFeedURL))
        if isDomId:
            divIncludedLinks = soup.find(id=domElement)
        else:
            divIncludedLinks = soup.find(class_=domElement)
        atag = divIncludedLinks.find_all("a")
        array = []

        for atag_data in atag:
            if baseURL in atag_data.get('href'):
                articleLink = atag_data.get('href')
            else:
                articleLink = baseURL + atag_data.get('href')
            data = {'link': articleLink, 'title': atag_data.getText()}
            array.insert(0, data)  # 更新日が古い順で配列にいれちえく

        feedRSS = generate_rss(title, newsFeedURL, array)
        return feedRSS


def generate_rss(title, newsFeedURL, array):
    fg = FeedGenerator()
    fg.title(title)
    fg.link(href=newsFeedURL, rel='alternate')
    fg.description(title + 'のnews Feed')
    fg.language('jp')

    # item追加 (title,link,(content))
    for item in array:
        entry = fg.add_entry()
        entry.title(item["title"])
        entry.link(href=item["link"])

    # Get the RSS feed as string
    rssfeed = fg.rss_str(pretty=True, encoding="UTF-8")
    return rssfeed


#scrape_html("https://www.city.shibuya.tokyo.jp/news/index.html?=news", "js-tabTarget")
