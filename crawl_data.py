from bs4 import BeautifulSoup
import urllib.request as rq_url
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from tqdm import tqdm as tqdm
import numpy as np
import os, glob
import csv
import urllib.parse
from multiprocessing.dummy import Pool as ThreadPool

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 
# request=rq_url.Request(url,None,headers)
def get_img(file_csv):
	#--- Read URLs from file
	# print('Processing ', file_csv)
	fold = file_csv.split('/')[-1].split('.')[0]
	if not os.path.isdir(os.path.join(csv_path, fold)):
		os.mkdir(os.path.join(csv_path, fold))
		# print('Create folder ', os.path.join(csv_path, fold))
	else:
		# print('Folder ', os.path.join(csv_path, fold), 'exist')
		pass
	with open(os.path.join(csv_path, file_csv), newline='') as csvfile:
		urls = list(csv.reader(csvfile))
		print('Found ', len(urls), 'urls in file ', file_csv)
	#--- Downloading
	count = 1
	path = '/home/kimtuthap97/Documents/synthesis/csv'
	for url in urls:
		# print('Processing ', url)
		url = str(url[0])
		url = urllib.parse.urljoin('https://', url)
		# url = url.replace(':', '%3A')
		# url = 'https://www.pinclipart.com/maxpin/xwhomx/'
		try:
			request=rq_url.Request(url,None,headers)
			page = rq_url.urlopen(request).read()
			soup = BeautifulSoup(page)
			images = soup.findAll('img')
			for image in tqdm(images):
				try:
					response = requests.get(image['src'])
					img = Image.open(BytesIO(response.content))
					if np.array(img).shape[-1]==4:
						# print('Downloading to ', os.path.join(path, fold, str(count)+'.png'))
						img.save(os.path.join(path, fold, str(count)+'.png'))
						# print('Hi shibe, ', count)
						count =count+1
				except:
					pass
		except:
			pass

if __name__ == '__main__':

	csv_path = '/home/kimtuthap97/Documents/synthesis/csv'
	list_csv = sorted(glob.glob(os.path.join(csv_path, '*.txt')))

	print('Found ', len(list_csv), ' csv file')
	pool = ThreadPool(12)
	for _ in tqdm(pool.imap_unordered(get_img, list_csv), total=len(list_csv)):
		pass

	
	
