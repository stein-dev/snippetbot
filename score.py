import hashlib
import requests
import json
import calendar
import datetime
import time
import argparse

device_string = "Android:8.1.0:Redmi Note 4:[si1=1080x1920,3.0]:e896c14c729e4c21"

header_str = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36"
mall_header = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36 SnippetMedia_Android"

api_score = "http://release-sg-api.snippetmedia.com/User/score?"
app_version = "3.4.5"
language = "en"

currentDT = datetime.datetime.now()

CYELLOW = '\033[93m'
CGREEN = '\33[32m'
CEND = '\033[0m'
CTITLE = '\x1b[6;30;42m'
CTEND = '\x1b[0m'

def get_token(token_file):
    try:
        f = open(token_file, "r")
        token = str(f.readline())
        return token
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close()  

def score(token_file):
    try:
        score_url = api_score + "token=" + get_token(token_file) + "&app_version=" + app_version + "&language=" + language + "&device_string=" + device_string    
        score_r = requests.get(score_url, headers={"User-Agent": mall_header})
        score_str1 = score_r.text
        score_str2 = json.loads(score_str1)
        if score_str2['error'] == 0:
            bp = score_str2['data']['balance_pb']
            bc = score_str2['data']['balance_coin']
            rate = score_str2['data']['rate']
            ap = score_str2['data']['accumulate_pb']
            ac = score_str2['data']['accumulate_coin']            
            yc = score_str2['data']['yesterday_coin']
            s = token_file.replace(".txt", "")     

            print(CTITLE + s +  " | Score | " + currentDT.strftime("%a, %b %d, %I:%M %p") + CTEND)
            print(CGREEN + "Peso: " + str(bp) + "\tTotal Peso: " + str(ap)  + CEND) 
            print(CGREEN + "Coin: " + str(bc) + "\tTotal Coin: " + str(ac) + CEND)
            print(CGREEN + "Rate: " + rate + "\tYsday Coin: " + str(yc) +CEND)                
    except ValueError as e:
        print(score_str1)
        print(e)

parser = argparse.ArgumentParser(description="SMBot by @pigscanfly - Automate everything in SnippetMedia")
parser.add_argument("-s", "--score", nargs=1, help ="Args: score | View coins/peso earnings.")
args = parser.parse_args()        

if args.score:
    token_file = args.score[0]
    score(token_file)
else:
    print("Invalid argument.")    