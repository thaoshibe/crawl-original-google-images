import argparse
import datetime
import json
import os
import sys
import time
import urllib
from multiprocessing.dummy import Pool as ThreadPool

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

def download_google_staticimages(searchword1):

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    #options.add_argument('--headless')
    dirs = searchword1
    if not os.path.join(path, dirs):
        os.mkdir(os.path.join(path, dirs))
    # searchword1 = 'henna'
    # searchword2 = 'art'
    # searchword3 = 'transparent'
    searchurl = 'https://www.google.com/search?q=' + searchword1 + '&source=lnms&tbm=isch'

    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        # print(f'No found chromedriver in this environment.')
        # print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    # print(f'Getting you a lot of images. This may take a few moments...')
    browser.find_elements_by_xpath("//*[contains(text(), 'Tools')]")[0].click()
    time.sleep(1)
    browser.find_elements_by_css_selector("[aria-label=Color]")[0].click()
    time.sleep(1)
    browser.find_elements_by_xpath("//*[contains(text(), 'Transparent')]")[0].click()
    time.sleep(1)
    element = browser.find_element_by_tag_name('body')
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    # print(f'Reached end of page.')
    time.sleep(0.5)
    # print(f'Retry')
    time.sleep(0.5)
    browser.find_element_by_xpath('//input[@value="Show more results"]').click()

    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    page_source = browser.page_source 

    soup = BeautifulSoup(page_source, 'lxml')
    images = soup.find_all('a')

    urls = []
    for image in tqdm(images):
        try:
            url = image['href']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['href']
                if not url.find('https://'):
                    # urls.append(image['src'])
                    pass
            except Exception as e:
                pass
    with open("./csv/{}.txt".format(searchword1), "w") as txt_file:
        for line in urls:
            txt_file.write("".join(line) + "\n")

    browser.close()
    # return count

# Main block
def main():
    list_keywords=['heart', 'watercolor', 'flower', 'tatoo design',
                    'henna', 'sticker', 'cute', 'daisy',
                    'leaf', 'rose', 'jewlery','gems', 'crystal']
    # for searchword1 in tqdm(list_keywords):

    #     download_google_staticimages(searchword1)
    #     print('Complete for {}, took {}'.format(searchword1, t1-t0))
    pool = ThreadPool(12)
    # pool.map()
    for _ in tqdm(pool.imap_unordered(download_google_staticimages, list_keywords), total=len(list_keywords)):
        pass
    pool.close()
    # total_time = t1 - t0
    # print(f'\n')
    # print(f'Download completed. [Successful count = {count}].')
    # print(f'Total time is {str(total_time)} seconds.')

if __name__ == '__main__':
    main()
