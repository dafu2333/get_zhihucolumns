import time
import re
import os
import requests
import w3lib.html
from bs4 import BeautifulSoup

def get_list():
    url = 'https://www.zhihu.com/api/v4/columns/%s/articles?include=data[*].topics&limit=10' % author
    article_dict = {}
    while True:
        print('fetching', url)
        try:
            resp = requests.get(url, headers=headers)
            j = resp.json()
            data = j['data']
        except:
            print('get list failed')

        for article in data:
            aid = article['id']
            akeys = article_dict.keys()
            if aid not in akeys:
                article_dict[aid] = article['title']

        if j['paging']['is_end']:
            break
        url = j['paging']['next']
        time.sleep(2)

    with open('zhihu_ids.txt', 'w') as f:
        items = sorted(article_dict.items())
        for item in items:
            f.write('%s %s\n' % item)

def get_txt(aid, title, index):
    file_name = '%03d. %s.txt' % (index, title)
    if os.path.exists(file_name):
        print(title, 'already exists.')
        return
    else:
        print('saving', title)
    try:
        url = 'https://zhuanlan.zhihu.com/p/' + aid
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='RichText ztext Post-RichText').prettify()
        content = w3lib.html.remove_tags(content)
        with open(file_name, 'w') as f:
            f.write(content)
    except:
        print('get failed', title)
    time.sleep(2)

def get_details():
    with open('zhihu_ids.txt') as f:
        i = 1
        for line in f:
            lst = line.strip().split(' ')
            aid = lst[0]
            title = '_'.join(lst[1:])
            get_txt(aid, title, i)
            i += 1
'''
def to_pdf():
    import pdfkit
    print('exporting PDF...')
    htmls = []
    for root, dirs, files in os.walk('.'):
        htmls += [name for name in files if name.endswith(".html")]
    pdfkit.from_file(sorted(htmls), author + '.pdf')
'''

if __name__ == '__main__':
    author = input('Please input author name:')
    headers = {
        'origin': 'https://zhuanlan.zhihu.com',
        'referer': 'https://zhuanlan.zhihu.com/%s' % author,
        'User-Agent': ('Mozilla/5.0'),
    }
    get_list()
    get_details()
    #to_pdf()
