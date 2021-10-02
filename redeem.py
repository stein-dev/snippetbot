import hashlib
import requests
import json
import calendar
import datetime
import time
import argparse
import schedule

device_string = "Android:8.1.0:Redmi Note 4:[si1=1080x1920,3.0]:e896c14c729e4c21"

header_str = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36"
mall_header = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36 SnippetMedia_Android"

api_score = "http://release-sg-api.snippetmedia.com/User/score?"
api_withdraw = "http://release-sg-api.snippetmedia.com/Cash/withdrawal?"
app_version = "3.4.5"
language = "en"
cash_type = "2"
str_cash = "100"

def get_token(token_file):
    try:
        f = open(token_file, "r")
        token = str(f.readline())
        return token
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close()  

def save_transaction(message):
    try:
        f = open("transaction.txt", "a")
        f.write(message)
    except FileNotFoundError as e:
        print(e)
    finally:
        f.close()          

def redeem(token_file):
    for i in range(45):
        try:        
            currentDT = datetime.datetime.now()
            dtime = currentDT.strftime("%a, %b %d, %I:%M:%S %p")
            url = api_withdraw + "token=" + get_token(token_file) + "&app_version=" + app_version + "&language=" + language + "&device_string=" + device_string + "&type=" + cash_type + "&cash=" + str_cash + "&remaing_id="+ cash_type
            r = requests.get(url, headers={"User-Agent": mall_header})
            str1 = r.text
            str2 = json.loads(str1)
            error_str = str2['error']
            if error_str == 0:
                message = token_file + " | " + str(i) + " | 100 | " + dtime
                print("\x1b[6;30;42m"  + message + "\x1b[0m")
                save_transaction(message)
                break            
            else:
                err_msg = str2['err_msg']
                message = token_file + " | " + str(i) + " | " + err_msg + " | " + str(dtime)
                print(message)
                time.sleep(4)          
        except ValueError as e:
            print(e)
            continue

def score(token_file):
    try:
        score_url = api_score + "token=" + get_token(token_file) + "&app_version=" + app_version + "&language=" + language + "&device_string=" + device_string    
        score_r = requests.get(score_url, headers={"User-Agent": mall_header})
        score_str1 = score_r.text
        score_str2 = json.loads(score_str1)
        if score_str2['error'] == 0:
            bp = float(score_str2['data']['balance_pb'])
            if bp >= 100:
                return True
            else:
                return False    
    except ValueError as e:
        print(e)            

parser = argparse.ArgumentParser(description="SMBot by @pigscanfly - Automate everything in SnippetMedia")
parser.add_argument("-r", "--redeem", nargs=1, help ="Args: redeem token_filename | Redeem P100 in CoinsPH.")
args = parser.parse_args()   

if args.redeem:
    token_file = args.redeem[0]
    if score(token_file) == True:
        redeem(token_file)
else:
    print("Invalid argument.")                    