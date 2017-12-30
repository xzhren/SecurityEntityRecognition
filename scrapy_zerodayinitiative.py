# coding: utf-8

import requests
import time
import re
from bs4 import BeautifulSoup
import os
import random
import traceback

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
# 'Connection':'keep-alive',
'Connection':'close',
'Cache-Control': 'no-cache',
'Accept-Language':'zh-CN,zh;q=0.8',
'Referer': 'http://central.maven.org/'
}

user_agent_list = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET4.0C)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; qihu theworld)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0; InfoPath.2)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.30729; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; GreenBrowser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 2345Explorer 4.2.0.13850)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 3.5.30729; Alexa Toolbar; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.4; KB974488)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; iCafeMedia; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; BIDUBrowser 2.x)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; baiduie8; 2345Explorer 4.2.0.13929)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; Apache; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; 360SE)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; 2345Explorer 5.0.0.14067)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/7.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/7.0; KB974488)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0) LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; QQBrowser/8.0.2820.400)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36 LBBROWSER",
        "Mozilla/5.0 (Windows NT 5.1; rv:32.0) Gecko/20100101 Firefox/32.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.12 (KHTML, like Gecko) Maxthon/3.0 Chrome/18.0.966.0 Safari/535.12",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36 CoolNovo/2.0.9.20",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 UBrowser/3.1.1644.34 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36 OPR/27.0.1689.76",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.2.0.3000 Chrome/30.0.1551.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; MALC; rv:11.0; QQBrowser/8.0.3345.400) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0; QQBrowser/8.0.3197.400) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.0.3000 Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3647.11 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "UCWEB/2.0 (Linux; U; Adr 2.3.5; zh-CN; Lenovo A288t) U2/1.0.0 UCBrowser/9.6.2.404 U2/1.0.0 Mobile",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
        "UCWEB/2.0 (MIDP-2.0; U; zh-CN; Lenovo S898t+) U2/1.0.0 UCBrowser/10.2.1.550  U2/1.0.0 Mobile",
        "UCWEB/2.0 (MIDP-2.0; U; zh-CN; MI 4C) U2/1.0.0 UCBrowser/10.2.0.535  U2/1.0.0 Mobile",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36 QQBrowser/3.3.3201.400",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; zh_cn) AppleWebKit/600.1.4.12.4 (KHTML, like Gecko) Version/5.0.5 Safari/600.1.4.12.4",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/7.1.3 Safari/537.85.12"
       ]

def key_to_file(key, html):
    file_name = key.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "-")\
        .replace("?", "-").replace("\"", "-").replace("|", "-").replace("<", "-").replace(">", "-")
    with open("zerodayinitiative/"+file_name, "w") as f:
        f.write(html.decode("utf-8"))

def get_html(url, counter):
    try:
        # proxys = filter_proxys()
        # proxies = random.choice(proxys)
        headers['User-Agent'] = random.choice(user_agent_list)
        # time.sleep(5)
        # with requests.get(url=url, headers=headers, proxies=proxies) as r:
        with requests.get(url=url, headers=headers) as r:
            return r.content
    except Exception as e:
        print("##########right exception", counter, url)
        time.sleep(30+counter)
        return None

def get_pages(url, baseurl):
    html = None
    counter = 0
    while html == None:
        html = get_html(url, counter)
        counter += 1

    key = url[len(baseurl):]
    key_to_file(key, html)
    # print("key:"+key)
    return

import _thread
import time
 
# ZDI-17-1009
# ZDI-16-700
def thread_fun( letter ):
    try:
        baseurl = 'http://www.zerodayinitiative.com/advisories/'
        for i in range(1, 700):
            if i < 10:
                no_str = "00"+str(i)
            elif i < 100:
                no_str = "0"+str(i)
            # elif i < 1000:
            else:
                no_str = str(i)
            url = 'http://www.zerodayinitiative.com/advisories/ZDI-16-' + no_str
            # print(url, end=",")
            print(url)
            get_pages(url, baseurl)
            time.sleep(1)
        # while 1:
        print("finished:"+letter)
        # with open("zero.txt", "a") as f:
        #     f.write(letter + " ")
    except Exception as e:
        traceback.print_exc()
        # while 1:
        #     print(letter, e)
        #     time.sleep(60)

thread_fun("a")
# range_list = [ord('a')]
# for i in range_list:
#     key = str(chr(i))
#     _thread.start_new_thread( thread_fun, (key,) )

# while 1:
#     pass
