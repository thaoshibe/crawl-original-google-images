import argparse
import csv
import glob
import json
import os

import cv2
import numpy as np
from mtcnn import MTCNN
from tqdm import tqdm

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--thumbnail_folder", default="/home/thaontp79/works/datasets/youtube-celeb/data/thumbnail", type=str, help='path to thumbnail')
    parser.add_argument("--output_dir", default="/home/thaontp79/works/datasets/youtube-celeb/data/mtcnn/json", type=str, help='path to save results')
    # parser.add_argument("--sa", action="store_true", default=False, help='whether to save meta data or not')
    # parser.add_argument("--download_video", default=False, action='store_true', help='whether to save video or not')
    # parser.add_argument("--thumbnail", default=False, action='store_true', help='whether to save thumbnail')
    # parser.add_argument("--pattern_only", default=False, action="store_true")
    args = parser.parse_args()

    print("           ⊱ ──────ஓ๑♡๑ஓ ────── ⊰")
    print("🎵 hhey, arguments are here if you need to check 🎵")
    for arg in vars(args):
        print("{:>15}: {:>30}".format(str(arg), str(getattr(args, arg))))
    print()
    return args

def write_csv(data):
	with open('/home/thaontp79/works/datasets/youtube-celeb/data/mtcnn/scores.csv', 'a') as outfile:
		writer = csv.writer(outfile)
		writer.writerow(data)

def rect_area(bbox):
	return bbox[-1]*bbox[-2]

def process_identity_subfolder(folder_path, detector):
	subfolder_rs = {}
	list_imgs = glob.glob(os.path.join(folder_path, '*.jpg'))
	count_face = 0
	total_face = 0
	for img_path in list_imgs:
		videoid = img_path.split('/')[-1][:-4]
		img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
		h, w, _ = img.shape
		faces = detector.detect_faces(img)

		video_rs = []
		for i, face in enumerate(faces):
			total_face+=1
			face['area'] = rect_area(face['box'])
			face['ratio'] = np.round(face['area']/(h*w), 3)
			#### TEST BLOCK
			if face['ratio']>0.2:
				count_face+=1
				img_save_path = os.path.join('/home/thaontp79/works/datasets/youtube-celeb/data/mtcnn/imgs', img_path.split('/')[-1])
				cv2.imwrite(img_save_path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
				write_csv([folder_path.split('/')[-1], videoid, face['ratio']])
			video_rs.append(face)
		subfolder_rs[videoid] = video_rs
	if total_face>0:
		print('Total: ', len(list_imgs), ' Faces: ', total_face, ' Ratio: ', np.round(count_face/total_face, 3)*100, '%')
	else:
		print('Total: ', len(list_imgs), ' Faces: ', total_face, ' Ratio: ', count_face)

	return subfolder_rs

if __name__ == "__main__":
	detector = MTCNN()
	# import pdb; pdb.set_trace()
	args = get_args()
	folder_names = os.listdir(args.thumbnail_folder)
	folder_paths = [os.path.join(args.thumbnail_folder, name) for name in folder_names]
	for i, folder_path in enumerate(tqdm(folder_paths)):
		subfolder_rs = process_identity_subfolder(folder_path, detector)
		output_file = os.path.join(args.output_dir, folder_names[i]+'.json')
		with open(output_file, 'w') as fp:
		    json.dump(subfolder_rs, fp)
