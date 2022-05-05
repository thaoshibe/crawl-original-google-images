import argparse
import csv
import datetime
import json
import os
import sys
import time
import urllib
from multiprocessing.dummy import Pool as ThreadPool

import numpy as np
import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm as tqdm
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

maxcount = 1000
path = '/home/thaontp79/works/datasets/tiktok/txt'
chromedriver = '/home/thaontp79/works/crawl-original-google-images/chromedriver_linux64/chromedriver'

def set_up_chrome(searchurl):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    element = browser.find_element_by_tag_name('body')

    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    page_source = browser.page_source 
    # print(f'Reached end of page.')
    time.sleep(0.5)
    return browser, page_source

def download_tiktok_urls(searchword1):
    #options.add_argument('--headless')
    dirs = searchword1
    if not os.path.join(path, dirs):
        os.mkdir(os.path.join(path, dirs))

    urls = []
    searchurl = 'https://www.tiktok.com/' + searchword1

    try:
        browser, page_source = set_up_chrome(searchurl)
        soup = BeautifulSoup(page_source, 'lxml')
        videos = soup.find_all('a')
        for video in videos:
            try:
                url = video['href']
                # print(url)
                if searchword1 in url:
                    urls.append(url)
            except Exception as e:
                pass
        browser.close()
    except Exception as e:
        print(e, searchword1)
        pass
    urls = np.unique(urls)

    with open(os.path.join(path, "{}.txt".format(searchword1)), "w") as txt_file:
        for line in urls:
            txt_file.write("".join(line) + "\n")

# Main block
def main():
    # list_keywords=['@hoaa.hanassii', '@charlidamelio', '@addisonre', '@zachking', '@lorengray']
    top100_file = '/home/thaontp79/works/datasets/tiktok/top100_clean.txt'
    with open(top100_file, newline='') as f:
        reader = csv.reader(f)
        list_names = list(reader)

    list_keywords = [x[0] for x in list_names]
    # for keyword in tqdm(list_keywords):
    #     download_tiktok_urls(keyword)
    pool = ThreadPool(4)
    for _ in tqdm(pool.imap_unordered(download_tiktok_urls, list_keywords), total=len(list_keywords)):
        pass
    pool.close()


if __name__ == '__main__':
    main()
