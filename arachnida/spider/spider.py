# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <2024_alex.sanchez@iticbcn.cat    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/27 14:03:32 by alexsanc          #+#    #+#              #
#    Updated: 2024/12/04 10:41:11 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import os
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def download_image(image_url, path):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type")
            if content_type and "image" in content_type:  # Ensure it is an image
                ext = os.path.splitext(image_url)[1]
                if not ext:  # If no extension, default to `.webp`
                    ext = ".webp"
                file_name = os.path.basename(image_url) or f"image{ext}"
                file_path = os.path.join(path, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print(f"Downloaded image: {image_url}")
            else:
                print(f"Skipped non-image URL: {image_url}")
        else:
            print(f"Error downloading image: {
                  response.status_code} - {image_url}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

def download_images(url, path, extensions, depth):
    """Recursively downloads all images from a URL and saves them to a local directory."""
    print(f"Processing URL: {url}, depth: {depth}")
    if depth == 0:
        return
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error processing URL: {url}, depth: {depth}, error: {e}")
        return
    if response.status_code != 200:
        print(f"Error processing URL: {url}, depth: {depth}, status code: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, "html.parser")
    print(f"Extensions: {extensions}")
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and any(src.endswith(ext) for ext in extensions):
            image_url = urljoin(url, src)
            print(f"Image URL: {image_url}")
            download_image(image_url, path)
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and urlparse(href).netloc == urlparse(url).netloc:
            print(f"Next URL: {href}")
            if not href.startswith("http"):
                href = urljoin(url, href)
            if not href.startswith("www"):
                href = href.replace("http://", "http://www.") or href.replace(
                    "https://", "https://www.")
            next_url = urljoin(url, href)
            print(f"Next URL: {next_url}")
            download_images(next_url, path, extensions, depth - 1)


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
        print("The path does not exist, do you want to create it? (y/n)")
        if input().lower() == "y":
            os.makedirs(args.path)
        else:
            return
    else:
        print("The path already exists, do you want to overwrite it? (y/n)")
        if input().lower() == "y":
            os.system("rm -rf " + args.path)
            os.makedirs(args.path)
        else:
            return
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".docx", ".pdf", ".webp"]
    download_images(args.url, args.path, extensions,
                    args.depth if args.recursive else 1)
    
    
    images = []
    failed_images_url = []
    retrieved_images_url = []
    urls = []
    failed_urls = []
    urls_parsed = []
    files_list = []
    files_failed_list = []

    if args.recursive:
        recursiveBool = "True"
    else:
        recursiveBool = "False"
        
    print("==========SPIDER RESULTS==========")
    print("URL: " + args.url)
    print("Recursive: " + recursiveBool)
    print("Depth: " + str(args.depth))
    print("Path: " + args.path)
    print("==================================")
    print("==========IMAGES RESULTS==========")
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith(tuple(extensions)):
                images.append(os.path.join(root, file))
    for image in images:
        if os.path.getsize(image) == 0:
            failed_images_url.append(image)
        else:
            retrieved_images_url.append(image)
    print("Retrieved images: " + str(len(retrieved_images_url)))
    print("Failed images: " + str(len(failed_images_url)))
    print("===================================")
    print("============URLS RESULTS===========")
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith(".html"):
                urls.append(os.path.join(root, file))
    for url in urls:
        with open(url, "r") as f:
            content = f.read()
            urls_parsed.append(re.findall(
                r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", content))
    for url in urls_parsed:
        for u in url:
            if u not in files_list:
                files_list.append(u)
    for url in files_list:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                retrieved_images_url.append(url)
            else:
                failed_urls.append(url)
        except:
            failed_urls.append(url)
    print("Retrieved urls: " + str(len(files_list)))
    print("Failed urls: " + str(len(failed_urls)))
    print("===================================")
    print("==========FILES RESULTS===========")
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith(tuple(extensions)):
                files_list.append(os.path.join(root, file))
    for file in files_list:
        if os.path.getsize(file) == 0:
            files_failed_list.append(file)
    print("Retrieved files: " + str(len(files_list)))
    print("Failed files: " + str(len(files_failed_list)))
    print("===================================")
    print("==========FAILED RESULTS==========")
    print("Failed images: " + str(len(failed_images_url)))
    print("Failed urls: " + str(len(failed_urls)))
    print("Failed files: " + str(len(files_failed_list)))
    print("===================================")
    print("==========RETRIEVED RESULTS==========")
    print("Retrieved images: " + str(len(retrieved_images_url)))
    print("Retrieved urls: " + str(len(files_list)))
    print("Retrieved files: " + str(len(files_list)))
    print("=====================================")
    print("==========TOTAL RESULTS==========")
    print("Total images: " + str(len(retrieved_images_url) + len(failed_images_url)))
    print("Total urls: " + str(len(files_list) + len(failed_urls)))
    print("Total files: " + str(len(files_list) + len(files_failed_list)))
    print("===================================")
    print("==========FAILED URLS==========")
    for url in failed_urls:
        print(url)
    else:
        print("0")
    print("===================================")
    print("==========FAILED IMAGES==========")
    for image in failed_images_url:
        print(image)
    else:
        print("0")
    print("===================================")
    print("==========FAILED FILES==========")
    for file in files_failed_list:
        print(file)
    else:
        print("0")
    print("===================================")
    print("==========RETRIEVED URLS==========")
    for url in files_list:
        print(url)
        # Print the web link that contains the image retrieved, but for every image
        
              
    print("===================================")
    print("==========RETRIEVED IMAGES==========")
    for image in retrieved_images_url:
        print(image)
    print("===================================")
    print("==========RETRIEVED FILES==========")
    for file in files_list:
        print(file)

if __name__ == "__main__":
    main()
