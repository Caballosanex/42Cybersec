# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/27 16:30:27 by alexsanc          #+#    #+#              #
#    Updated: 2023/05/03 16:35:43 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import io
import sys
import os
from datetime import datetime
from PIL import Image, ExifTags


def get_creation_time(file_path):
    if sys.platform == "darwin":
        stat = os.stat(file_path)
        return datetime.fromtimestamp(stat.st_ctime)
    
def get_user(file_path):
    if sys.platform == "darwin":
        stat = os.stat(file_path)
        return stat.st_uid

def get_group(file_path):
    if sys.platform == "darwin":
        stat = os.stat(file_path)
        return stat.st_gid

def get_size(file_path):
    if sys.platform == "darwin":
        stat = os.stat(file_path)
        return stat.st_size

def get_access_time(file_path):
    if sys.platform == "darwin":
        stat = os.stat(file_path)
        return datetime.fromtimestamp(stat.st_atime)
    
def get_modification_time(file_path):
    if sys.platform == "darwin":
        stat = os.stat(file_path)
        return datetime.fromtimestamp(stat.st_mtime)


def print_metadata(file_path):
    print(f"File: {file_path}")
    file_format = os.path.splitext(file_path)[1]
    print(f"  File Format: {file_format}")
    print(f"  Date Created: {get_creation_time(file_path)}")
    print(f"  User: {get_user(file_path)}")
    print(f"  Group: {get_group(file_path)}")
    print(f"  Size: {get_size(file_path)}")
    print(f"  Date Accessed: {get_access_time(file_path)}")
    print(f"  Date Modified: {get_modification_time(file_path)}")
    
    with Image.open(file_path) as img:
        exif_data = img.getexif()
        if exif_data:
            for tag_id in exif_data:
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                tag_value = exif_data.get(tag_id)
                if isinstance(tag_value, bytes):
                    tag_value = tag_value.decode()
                print(f"  {tag_name}: {tag_value}")


if __name__ == '__main__':
    for file_path in sys.argv[1:]:
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            continue
        try:
            print_metadata(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")