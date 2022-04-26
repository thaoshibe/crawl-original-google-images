import argparse
import csv
import glob
import os
import pickle
import urllib.request
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

import pafy
from tqdm import tqdm as tqdm


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--txt_folder", default="/home/thaontp79/works/datasets/youtube-celeb/urls", type=str, help='path to urls folder')
    parser.add_argument("--output_path", default="/home/thaontp79/works/datasets/youtube-celeb/data", type=str, help='path to save results')
    parser.add_argument("--metadata", action="store_true", default=False, help='whether to save meta data or not')
    parser.add_argument("--download_video", default=False, action='store_true', help='whether to save video or not')
    parser.add_argument("--thumbnail", default=False, action='store_true', help='whether to save thumbnail')
    # parser.add_argument("--pattern_only", default=False, action="store_true")
    args = parser.parse_args()

    print("           ⊱ ──────ஓ๑♡๑ஓ ────── ⊰")
    print("🎵 hhey, arguments are here if you need to check 🎵")
    for arg in vars(args):
        print("{:>15}: {:>30}".format(str(arg), str(getattr(args, arg))))
    print()
    return args


def download(txt_file, output_path='.', download_video=False, metadata=False, thumbnail=False):
	identity = txt_file.split('/')[-1][:-4]
	save_video_dir = os.path.join(output_path, 'videos', identity)
	metadata_dir = os.path.join(output_path, 'metadata', identity)
	thumb_dir = os.path.join(output_path, 'thumbnail', identity)

	for folder in [save_video_dir, metadata_dir, thumb_dir]:
		if not os.path.isdir(folder):
			os.makedirs(folder)

	with open(txt_file, newline='') as f:
	    reader = csv.reader(f)
	    list_urls = list(reader)

	for url in list_urls:
		try:
			# print('Dowloadin: ', url)
			url = 'https://www.youtube.com'+url[0]
			video = pafy.new(url)
			if download_video:
				path_to_save= os.path.join(save_video_dir, str(video.videoid)+'.mp4')
				bestResolutionVideo = video.getbest(preftype="mp4")
				bestResolutionVideo.download(quiet=True, filepath = path_to_save)
			if metadata:
				infor = video._ydl_info
				save_dir = os.path.join(metadata_dir, video.videoid +'.pkl')
				with open(save_dir, 'wb') as f:
					pickle.dump(infor, f)
				if thumbnail:
					# import pdb; pdb.set_trace()
					save_dir = os.path.join(thumb_dir, video.videoid+ video.bigthumbhd[-4:])
					urllib.request.urlretrieve(video.bigthumbhd, save_dir)
				# import pdb; pdb.set_trace()
		except Exception as e:
			print(e, url)

if __name__ == "__main__":
	args = get_args()
	
	list_txt = glob.glob(os.path.join(args.txt_folder, '*.txt'))
	print('Processing ', list_txt)
	# download(list_txt[0], output_path=args.output_path, download_video=args.download_video, metadata=args.metadata, thumbnail=args.thumbnail)
	pool = ThreadPool(4)
	func = partial(download, output_path=args.output_path, download_video=args.download_video, metadata=args.metadata, thumbnail=args.thumbnail)
	for _ in tqdm(pool.imap_unordered(func, list_txt), total=len(list_txt)):
		pass
