'''
Author: dota_st
blog: www.wlhhlc.top
'''
import requests
import re
import configparser
import json
import warnings
import os
import urllib.parse
warnings.filterwarnings("ignore")
config = configparser.ConfigParser()
config.read("config.ini")

def old_file_read(file_name):
    file = open("./old_file/"+file_name, 'r', encoding="utf-8").read()
    file = urllib.parse.unquote(file)
    return file

def get_image(file_name):
    short_file_name = file_name.split(".")[0]
    file_content = old_file_read(file_name)
    img_pattern = r'(!\[.*?\]\({0}\.assets/image-.*?.png\))'.format(short_file_name)
    image_list = re.findall(img_pattern, file_content)
    return image_list

def upload_img(file_name):
    img_list = get_image(file_name)
    dir_list = []
    img_path_list = []
    for i in img_list:
        short_file_name = file_name.split(".")[0]
        img_pattern = r'({0}\.assets/image-.*?.png)'.format(short_file_name)
        dir = re.findall(img_pattern, i)
        print(dir)
        dir_list.extend(dir)
    for i in dir_list:
        i = str(i)
        real_file = "./old_file/" + i
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Host": "forum.butian.net",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "X-CSRF-TOKEN": config['settings']['X-CSRF-TOKEN'],
        "Connection": "close",
        "Referer": "https://forum.butian.net/share/create",
        "Cookie": config['settings']['cookie']
        }
        pattern = r"(image-.*?.png)"
        img_name = re.search(pattern, i).group()
        res = requests.post(url="https://forum.butian.net/image/uploadS3", headers=headers, files ={"file": open(real_file,"rb")}, verify=False)
        img_url = res.text
        print(f"\033[1;35m[+]{file_name} upload success! >> \033[0m" + img_url)
        img_path = f"![{img_name}]" + f"({img_url})"
        img_path_list.append(img_path)
    return img_path_list
    

def custom_make_translation(text, translation):
    regex = re.compile('|'.join(map(re.escape, translation)))
    return regex.sub(lambda match: translation[match.group(0)], text)

def create_file(file_name):
    content = old_file_read(file_name)
    img_list = get_image(file_name)
    if img_list:
        path_list = upload_img(file_name)
        dicts = dict()
        for i,j in zip(img_list,path_list):
            dicts[i]=j
        content = custom_make_translation(content, dicts)
    new_file = open("./new_file/"+file_name, 'w')
    print(f"\033[1;32m[ok]{file_name} create success!\033[0m")
    new_file.write(content)

def main():
    file_list = os.listdir("./old_file/")
    files = "  ".join(file_list)
    logo = r"""
   ____                            _   _      _      
  / __ \                /\        | | (_)    | |     
 | |  | | __ ___  __   /  \   _ __| |_ _  ___| | ___ 
 | |  | |/ _` \ \/ /  / /\ \ | '__| __| |/ __| |/ _ \
 | |__| | (_| |>  <  / ____ \| |  | |_| | (__| |  __/
  \___\_\\__,_/_/\_\/_/    \_\_|   \__|_|\___|_|\___|
                                        
Powered by dota_st
Blog's: https://www.wlhhlc.top/
"""
    print(logo)
    print(f"\033[1;34m[*]scan file_dir: {files}\033[0m")
    for i in file_list:
        if os.path.exists("./new_file/" + i):
            pass
        elif ".assets" in i:
            pass
        else:
            create_file(i)

if __name__ == '__main__':
    main()