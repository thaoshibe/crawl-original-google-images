# Crawl Original Google Images & Youtube Videos

---

This repo contains code to crawl images and videos:
- ORIGINAL images from Google Search
- ORIGINAL videos from Youtube

### Requirements

1. **ChromeDriver**
	- [Check your current Google Chrome Version](https://www.businessinsider.com/what-version-of-google-chrome-do-i-have)
	- Download ChromeDriver corresponding to your Chrome Version at [ChromeDriver](https://chromedriver.chromium.org/downloads), unzip it.

	For example, I'm using Chrome Version `95.0.4638.69`, Linux, so I downloaded [`chromedriver_linux64.zip`](https://chromedriver.storage.googleapis.com/index.html?path=95.0.4638.69/)
1. **Enviroments**
	`conda env create -f environment.yml`

### Crawl Images from Google Image Search

Download original (not thumbnails) from Google Images Search with **multi-threading** :D
1. Get URLs by keywords
	```
		python crawl_url.py
	```
1. Download imgs from URLs
	```
		python crawl_data.py
	```

### Crawl Videos from Youtube
1. Get URLs by keywords
	```
	python crawl_youtube_link.py
	```
1. Download videos from URLs
	```
	python crawl_videos.py
	python crawl_videos.py --metadata --thumbnail # thumbnail and metadata only
	```

##### To-do
- [x] Init
- [x] Multithreading
- [x] Requiremets
- [x] Write Guideline
- [ ] Add parser to save_dirs, chromedriver, etc.