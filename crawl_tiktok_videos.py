import argparse
import csv
import glob
import os
import time
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

from TikTokApi import TikTokApi
from tqdm import tqdm as tqdm


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--txt_folder", default="/home/thaontp79/works/datasets/tiktok/txt", type=str, help='path to urls folder')
	parser.add_argument("--output_path", default="/home/thaontp79/works/datasets/tiktok/videos", type=str, help='path to save results')
	# parser.add_argument("--n_videos", default=1000, type=int, help='number of videos for each hashtag')
	args = parser.parse_args()

	print("           ⊱ ──────ஓ๑♡๑ஓ ────── ⊰")
	print("🎵 hhey, arguments are here if you need to check 🎵")
	for arg in vars(args):
		print("{:>15}: {:>30}".format(str(arg), str(getattr(args, arg))))
	print()
	return args

def get_video_by_id(video_ids, userid, output_path, api):
	folder_by_id = os.path.join(output_path, userid)
	if not os.path.isdir(folder_by_id):
		os.makedirs(folder_by_id)

	for videoid in tqdm(video_ids):
		save_dir = os.path.join(folder_by_id, "{}.mp4".format(videoid))
		try:
			'''
			get video: 10^-6s
			video bytes: 3.11s
			video info: 1.1s
			-> filter by video info
			'''

			video = api.video(id=videoid)
			video_info = video.info()
			ratio = video_info['video']['ratio']
			# w, h = video_info['video']['width'], video_info['video']['height']
			if (ratio in ['720p', '1080p', '1080i', '2160p']):
				with open(save_dir, "wb") as out_file:
					video_data = video.bytes()
					out_file.write(video_data)
			else:
				print('Passing: ', videoid, ratio)
		except Exception as e:
			print(e)
	# return None

def process_txt(txt_file, args, api):
	with open(txt_file, newline='') as f:
		reader = csv.reader(f)
		list_urls = list(reader)

	video_ids = [x[0].split('/')[-1] for x in list_urls]
	userid = list_urls[0][0].split('/')[-3]
	get_video_by_id(video_ids, userid, args.output_path, api)
	# return None

if __name__ == '__main__':

	args = get_args()
	txt_files = glob.glob(os.path.join(args.txt_folder, '*.txt'))
	api = TikTokApi()
	process_txt(txt_files[1], args, api)
	# func = partial(process_txt, args=args, api=api)
	# pool = ThreadPool(4)
	# for _ in tqdm(pool.imap_unordered(func, txt_files), total=len(txt_files)):
	# 	pass
