import argparse
import csv
import glob
import os
from multiprocessing.dummy import Pool as ThreadPool

import pafy
from tqdm import tqdm as tqdm


def download(txt_file, output_path='/home/thaontp79/works/datasets/youtube-celeb/videos'):
	identity = txt_file.split('/')[-1].split('.')[0]
	save_video_dir = output_path +'/'+'{}'.format(identity)

	if not os.path.isdir(save_video_dir):
		os.makedirs(save_video_dir)
	print('Saving in: ', save_video_dir)

	with open(txt_file, newline='') as f:
	    reader = csv.reader(f)
	    list_urls = list(reader)

	for url in tqdm(list_urls):
		try:
			url = 'https://www.youtube.com'+url[0]
			video = pafy.new(url)
			path_to_save= os.path.join(save_video_dir, str(video.videoid)+'.mp4')
			bestResolutionVideo = video.getbest(preftype="mp4")
			bestResolutionVideo.download(quiet=False, filepath = path_to_save)
		except Exception as e:
			print(e, url)

if __name__ == "__main__":
	
	list_txt = glob.glob(os.path.join('/home/thaontp79/works/datasets/youtube-celeb/urls', '*.txt'))
	print('Processing ', list_txt)

	# download(list_txt[0])
	pool = ThreadPool(2)
	for _ in tqdm(pool.imap_unordered(download, list_txt), total=len(list_txt)):
		pass
