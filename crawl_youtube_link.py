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
path = '/home/kimtuthap97/Documents/synthesis'
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

    browser.find_elements_by_xpath("//*[contains(text(), 'Filters')]")[0].click()
    time.sleep(1)
    browser.find_elements_by_xpath("//*[contains(text(), 'Under 4 minutes')]")[0].click()
    time.sleep(1)
    browser.find_elements_by_xpath("//*[contains(text(), 'Filters')]")[0].click()
    time.sleep(1)
    browser.find_elements_by_xpath("//*[contains(text(), 'HD')]")[0].click()
    time.sleep(1)
    element = browser.find_element_by_tag_name('body')

    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    page_source = browser.page_source 
    # print(f'Reached end of page.')
    time.sleep(0.5)
    return browser, page_source

def download_youtube_urls(searchword1):
    #options.add_argument('--headless')
    dirs = searchword1
    if not os.path.join(path, dirs):
        os.mkdir(os.path.join(path, dirs))

    urls = []
    # normal words
    searchurl = 'https://www.youtube.com/results?search_query=' + searchword1

    try:
        browser, page_source = set_up_chrome(searchurl)
        soup = BeautifulSoup(page_source, 'lxml')
        videos = soup.find_all('a')

        for video in videos:
            try:
                url = video['href']
                if '/watch?v' in url:
                    urls.append(url)
            except Exception as e:
                pass

        browser, page_source = set_up_chrome(searchurl + ' interview')
        soup = BeautifulSoup(page_source, 'lxml')
        videos = soup.find_all('a')

        # urls = []
        for video in tqdm(videos):
            try:
                url = video['href']
                if '/watch?v' in url:
                    urls.append(url)
            except Exception as e:
                pass
        browser.close()
    except Exception as e:
        print(e, searchword1)
        pass
    urls = np.unique(urls)

    with open("/home/thaontp79/works/datasets/youtube-celeb/urls/{}.txt".format(searchword1), "w") as txt_file:
        for line in urls:
            txt_file.write("".join(line) + "\n")

# Main block
def main():
    # list_keywords=['Gilbert Gottfried', 'Joseph Gatt', 'Alexander Skarsgård',
    #             'Simone Ashley', 'Nicola Peltz Beckham', 'Amber Heard',
    #             'Oscar Isaac', 'Emma Mackey', 'Jonathan Bailey',
    #             'May Calamawy']
    ijbc_file = '/home/thaontp79/works/datasets/youtube-celeb/ijbc_subject_names.csv'
    with open(ijbc_file, newline='') as f:
        reader = csv.reader(f)
        list_names = list(reader)
    list_keywords = [x[1] for x in list_names[1:]]

    pool = ThreadPool(4)
    for _ in tqdm(pool.imap_unordered(download_youtube_urls, list_keywords), total=len(list_keywords)):
        pass
    pool.close()
    # for keyword in list_keywords:
    #     download_youtube_urls(keyword)


if __name__ == '__main__':
    main()
