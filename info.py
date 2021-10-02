import hashlib
import requests
import json
import calendar
import datetime
import time
import argparse


device_string = "Android:8.1.0:Redmi Note 4:[si1=1080x1920,3.0]:c53db51abd8a8098"

header_str = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36"
mall_header = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36 SnippetMedia_Android"

api_score = "http://release-sg-api.snippetmedia.com/User/score?"
api_refer = "http://release-sg-api.snippetmedia.com/MentoringActivity/inviter_detail?"
api_userinfo = "http://release-sg-api.snippetmedia.com/User/info?"

app_version = "3.4.5"
language = "en"
release_key = "u5kC9lODPmeHW2KbzCWCI9BlO4xHrxo4"

currentDT = datetime.datetime.now()

CYELLOW = '\033[93m'
CGREEN = '\33[32m'
CEND = '\033[0m'
CTITLE = '\x1b[6;30;42m'
CTEND = '\x1b[0m'
         
refer_id = ""

def get_token(token_file):
    try:
        f = open(token_file, "r")
        token = str(f.readline())
        return token
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close()  

def user_info(token_file):
    timestamp = calendar.timegm(time.gmtime())
    sign_one_str = app_version + device_string + language + str(timestamp) + get_token(token_file) + refer_id + release_key
    sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
    sign_one_final = sign_one_md5.hexdigest().upper()

    url = api_userinfo + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&timestamp=" + str(timestamp) + "&token=" + get_token(token_file) + "&userid=" + refer_id

    req = requests.get(url, headers={"User-Agent": header_str})
    req_str = req.text
    req_json = json.loads(req_str)
    error_str = req_json['error']
    if error_str == 0:
        info_id = req_json['data']['userid']
        info_uname = req_json['data']['user_name']
        info_phone = req_json['data']['phone']
        print(CGREEN + "UserID:    " +  str(info_id) + CEND)
        print(CGREEN + "Username:  " + str(info_uname) + CEND)
        print(CGREEN + "Phone:     " + str(info_phone) + CEND)  

def get_refer_code(token_file):
    global refer_id
    url = api_refer + "token=" + get_token(token_file) + "&app_version=" + app_version + "&language=" + language + "&device_string=" + device_string    
    req = requests.get(url)
    req_str = req.text
    req_json = json.loads(req_str)
    error_str = req_json['error']
    if error_str == 0:
        refer_id = req_json['data']['user_id']
        refer_code = req_json['data']['code']
        s = token_file.replace(".txt", "")  
        print(CTITLE + s + " | Info | " + currentDT.strftime("%a, %b %d, %I:%M:%S %p") + CTEND)  
        print(CGREEN + "Code:      " + str(refer_code) + CEND)
    else:
        print(url)
        print(req_str)    

parser = argparse.ArgumentParser(description="SMBot by @pigscanfly - Automate everything in SnippetMedia")
parser.add_argument("-i", "--info", nargs=1, help ="Args: info | View account info.")
args = parser.parse_args()        

if args.info:
    token_file = args.info[0]
    get_token(token_file)
    get_refer_code(token_file)
    user_info(token_file)
else:
    print("Invalid argument.")    