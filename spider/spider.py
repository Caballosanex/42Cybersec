# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/27 14:03:32 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/27 14:23:09 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import os
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def download_image(image_url, path):
    """Downloads an image from a URL to a local directory."""
    response = requests.get(image_url)
    filename = os.path.join(path, os.path.basename(urlparse(image_url).path))
    with open(filename, "wb") as f:
        f.write(response.content)

def download_images(url, path, extensions, depth):
    """Recursively downloads all images from a URL and saves them to a local directory."""
    if depth == 0:
        return
    try:
        response = requests.get(url)
    except:
        return
    soup = BeautifulSoup(response.content, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and any(src.endswith(ext) for ext in extensions):
            image_url = urljoin(url, src)
            download_image(image_url, path)
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and urlparse(href).netloc == urlparse(url).netloc:
            next_url = urljoin(url, href)
            download_images(next_url, path, extensions, depth-1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL to download images from")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="recursively download images from subpages")
    parser.add_argument("-l", "--depth", type=int, default=5,
                        help="maximum recursion depth")
    parser.add_argument("-p", "--path", default="./data/",
                        help="path to save downloaded files")
    args = parser.parse_args()
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tif", ".tiff", ".jfif", ".pjpeg", ".pjp", ".avif", ".apng", ".avif"]
    download_images(args.url, args.path, extensions, args.depth if args.recursive else 1)

if __name__ == "__main__":
    main()
