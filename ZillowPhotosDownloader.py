import os
import re
import sys
import requests
import argparse
from bs4 import BeautifulSoup
from datetime import datetime

def preprocess_html(content):
    start_marker = "compsCarouselPropertyPhotos"
    start_index = content.find(start_marker)
    
    if start_index != -1:
        reversed_content = content[::-1]
        reversed_end_index = reversed_content.find(start_marker[::-1])
        if reversed_end_index != -1:
            end_index = len(content) - reversed_end_index - len(start_marker)
            content = content[:start_index] + content[end_index + len(start_marker):]
    return content

def download_zillow_images(url, append_date, jpg_flag):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    session.headers.update(headers)

    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage: {response.status_code}")
        return

    processed_content = preprocess_html(response.text)

    soup = BeautifulSoup(processed_content, 'html.parser')
    title_tag = soup.find('title')
    if not title_tag:
        print("Failed to find the page title for address")
        return

    address = title_tag.text.split("|")[0].strip()
    directory_name = address
    if append_date:
        today = datetime.now().strftime("%Y-%m-%d")
        directory_name += f" - {today}"

    directory = os.path.join(os.getcwd(), directory_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    ext = 'jpg' if jpg_flag else 'webp'
    pattern = re.compile(rf'(https://photos.zillowstatic.com/fp/([0-9a-f]{{32}})-cc_ft_(\d+).{ext})')

    image_urls = set(re.findall(pattern, str(soup)))

    highest_res_images = {}
    for full_url, photo_id, resolution in image_urls:
        if photo_id not in highest_res_images or int(highest_res_images[photo_id][1]) < int(resolution):
            highest_res_images[photo_id] = (full_url, resolution)

    for photo_id, (url, resolution) in highest_res_images.items():
        image_response = session.get(url)
        if image_response.status_code == 200:
            image_name = f"{photo_id}-cc_ft_{resolution}.{ext}"
            with open(os.path.join(directory, image_name), 'wb') as f:
                f.write(image_response.content)
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download image from {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Zillow listing images.')
    parser.add_argument('url', help='Zillow listing URL')
    parser.add_argument('-d', '--date', action='store_true', help='Append the current date to the directory name')
    parser.add_argument('-j', '--jpg', action='store_true', help='Download images in JPG format instead of WEBP')
    args = parser.parse_args()

    download_zillow_images(args.url, args.date, args.jpg)