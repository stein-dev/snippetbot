import hashlib
import requests
import json
import calendar
import datetime
import time
import random
import argparse
import os

app_type = "android-lite"
app_version = "1.0.2"
area_code = "+63"
device_string = "Android:7.1.1:SC-04E:[si1=1280x720,1.5]:3ab2e278c015fb01"
language = "en"
release_key = "u5kC9lODPmeHW2KbzCWCI9BlO4xHrxo4"
device_type = "android"
dev_type = "android-lite"

bind_phone_url = "http://release-sg-api.snippetmedia.com/TaskCenter/bind_phone?"
api_refer = "http://release-sg-api.snippetmedia.com/MentoringActivity/inviter_detail?"

header_str = "Mozilla/5.0 (Linux; Android 5.1.1; A33fw Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"
invite_header = "Mozilla/5.0 (Linux; Android 5.1.1; A33fw Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Safari/537.36 SnippetMedia_Android"

mobile = ""
token = ""
code = ""
timestamp = ""
ref_code = ""
filename = ""
refer_id = ""

CYELLOW = '\033[93m'
CGREEN = '\33[32m'
CEND = '\033[0m'



def get_token(token_file):
    try:
        f = open(token_file, "r")
        token = str(f.readline())
        return token
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close()  

def get_refer_code(token_file):
    global refer_id
    url = api_refer + "token=" + get_token(token_file) + "&app_version=" + app_version + "&language=" + language + "&device_string=" + device_string    
    req = requests.get(url)
    req_str = req.text
    req_json = json.loads(req_str)
    error_str = req_json['error']
    if error_str == 0:
        refer_id = req_json['data']['user_id']
        print(refer_id)
    else:
        print(url)
        print(req_str)           

def bind_phone(token_file):
    sign_one = app_version + device_string + language + \
        str(calendar.timegm(time.gmtime())) + get_token(token_file) + refer_id + release_key
    sign_one_md5 = hashlib.md5(sign_one.encode("utf-8"))
    sign_one_final = sign_one_md5.hexdigest().upper()

    url = bind_phone_url + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + \
        "&language=" + language + "&timestamp=" + \
        str(calendar.timegm(time.gmtime())) + \
        "&token=" + get_token(token_file) + "&userid=" + refer_id

    req = requests.get(url, headers={"User-Agent": header_str})
    req_txt = req.text
    req_json = json.loads(req_txt)
    print(req_txt)
    if req_json['error'] == 0:
        text = req_json['data']['text']
        print(text)
    else:
        print(req_txt)


parser = argparse.ArgumentParser(description="SMBot by @pigscanfly - Automate everything in SnippetMedia")
parser.add_argument("-b", "--bind", nargs=1, help ="Args: bind | Bind account.")
args = parser.parse_args()        

if args.bind:
    token_file = args.bind[0]
    get_refer_code(token_file)
    bind_phone(token_file)
else:
    print("Invalid argument.")           