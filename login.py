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

get_token_url = "http://release-sg-api.snippetmedia.com/Token/get_device_token?"
send_code_url = "http://release-sg-api.snippetmedia.com/SignIn/send_login_code?"
login_url = "http://release-sg-api.snippetmedia.com/SignIn/login?"
get_info_url = "http://release-sg-api.snippetmedia.com/GlobalConfig/get_info?"
bind_phone_url = "http://release-sg-api.snippetmedia.com/TaskCenter/bind_phone?"
bind_code_url = "http://release-sg-api.snippetmedia.com/Invite/bind_code?"

header_str = "Mozilla/5.0 (Linux; Android 5.1.1; A33fw Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"
invite_header = "Mozilla/5.0 (Linux; Android 5.1.1; A33fw Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Safari/537.36 SnippetMedia_Android"

mobile = ""
token = ""
code = ""
timestamp = ""
ref_code = ""
filename = ""

CYELLOW = '\033[93m'
CGREEN = '\33[32m'
CEND = '\033[0m'

def set_filename():
    global filename
    try:
        while True:
            fname = input("Enter filename: ")
            if not fname:
                continue
            else:
                tmp = fname + ".txt"
                if os.path.exists(tmp) == True:
                    print(CYELLOW + "File already exist" + CEND)
                    continue
                else:
                    f = open(tmp, "w")
                    if os.path.exists(tmp) == True:
                        print(CGREEN + "File created: " + tmp + CEND)
                        filename = tmp
                        break
    except FileExistsError as e:
        print(e)   
    finally:
        f.close()
        
def get_info():
    try:
        global timestamp
        sign_one = app_type + app_version + device_string + \
            language + dev_type + language + release_key
        sign_one_md5 = hashlib.md5(sign_one.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()

        url = get_info_url + "_sign=" + sign_one_final + "&app_type=" + app_type + "&app_version=" + \
            app_version + "&device_string=" + device_string + \
            "&device_type=" + dev_type + "&language=" + language

        req = requests.get(url, headers={"User-Agent": header_str})
        req_txt = req.text
        req_json = json.loads(req_txt)
        if req_json['error'] == 0:
            timestamp = req_json['data']['timestamp']
            print(CGREEN + "Timestamp: " + str(timestamp) + CEND)
        else:
            print(CYELLOW + req_txt + CEND)
            exit()
    except ValueError as e:
        print(e)    

def get_token():
    global token
    global timestamp
    sign_two = device_string + release_key
    sign_two_md5 = hashlib.md5(sign_two.encode("utf-8"))
    sign_two_final = sign_two_md5.hexdigest().lower()

    sign_one = app_type + app_version + device_string + \
        language + sign_two_final + str(timestamp) + release_key
    sign_one_md5 = hashlib.md5(sign_one.encode("utf-8"))
    sign_one_final = sign_one_md5.hexdigest().upper()

    token_url = get_token_url + "_sign=" + sign_one_final + "&app_type=" + app_type + "&app_version=" + app_version + \
        "&device_string=" + device_string + "&language=" + language + \
        "&sign=" + sign_two_final + "&timestamp=" + str(timestamp)

    req = requests.get(token_url, headers={"User-Agent": header_str})
    req_txt = req.text
    req_json = json.loads(req_txt)
    if req_json['error'] == 0:
        token = req_json['data']['token']
        print("Token: " + token)            

def input_mobile():
    global mobile
    while True:
        try:
            mobile = str(input("Enter mobile +63: "))
            if not mobile:
                continue
            elif mobile.isdigit() and len(mobile) == 10:
                print("Mobile: ", mobile)
                break
        except ValueError as e:
            print(e)
            break

def send_code():
    try:
        global timestamp
        sign_two = mobile + release_key
        sign_two_md5 = hashlib.md5(sign_two.encode("utf-8"))
        sign_two_final = sign_two_md5.hexdigest().lower()

        sign_one = app_type + app_version + area_code + device_string + language + \
            mobile + sign_two_final + str(timestamp) + token + release_key
        sign_one_md5 = hashlib.md5(sign_one.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()

        login_code_url = send_code_url + "_sign=" + sign_one_final + "&app_type=" + app_type + "&app_version=" + app_version + "&area_code=" + area_code + \
            "&device_string=" + device_string + "&language=" + language + "&mobile=" + mobile + \
            "&sign=" + sign_two_final + "&timestamp=" + \
            str(timestamp) + "&token=" + token

        req = requests.get(login_code_url, headers={"User-Agent": header_str})
        req_txt = req.text
        req_json = json.loads(req_txt)
        if req_json['error'] == 0:
            print(CGREEN + "Code sent!" + CEND)
        else:
            print(CYELLOW + req_txt + CEND)
            exit()
    except ValueError as e:
        print(e)    

def input_code():
    global code
    while True:
        try:
            code = str(input("Enter code: "))
            if not code:
                continue 
            else:
                print("Code: ", code)
                break    
        except ValueError as e:
            print(e)
           

def login():
    try:
        sign_two = mobile + release_key
        sign_two_md5 = hashlib.md5(sign_two.encode("utf-8"))
        sign_two_final = sign_two_md5.hexdigest().lower()

        sign_one = app_type + app_version + area_code + code + device_string + \
            language + mobile + sign_two_final + \
            str(timestamp) + token + release_key
        sign_one_md5 = hashlib.md5(sign_one.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()

        url = login_url + "_sign=" + sign_one_final + "&app_type=" + app_type + "&app_version=" + app_version + "&area_code=" + area_code + "&code=" + code + \
            "&device_string=" + device_string + "&language=" + language + "&mobile=" + mobile + \
            "&sign=" + sign_two_final + "&timestamp=" + \
            str(timestamp) + "&token=" + token

        req = requests.get(url, headers={"User-Agent": header_str})
        req_txt = req.text
        req_json = json.loads(req_txt)
        if req_json['error'] == 0:
            userid = req_json['data']['userid']
            new_token = req_json['data']['token']
            f = open(filename, "w")
            f.write(new_token + "\n")
            f.write(userid + "\n")
            print(CGREEN + "New Token: " + new_token + CEND)
            print(CGREEN + "UserID: " + userid + CEND)
        else:
            print(req_txt)
    except ValueError as e:
        print(e)        

def get_login_token():
    try:
        f = open("login.txt", "r")
        lines = f.readlines()
        ntoken = str(lines[0])
        return ntoken
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close()  

def get_login_userid():
    try:
        f = open("login.txt", "r")
        lines = f.readlines()
        userid = str(lines[1])
        return userid
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close() 
        
def bind_phone():
    sign_one = app_version + device_string + language + \
        str(calendar.timegm(time.gmtime())) + get_login_token() + get_login_userid() + release_key
    sign_one_md5 = hashlib.md5(sign_one.encode("utf-8"))
    sign_one_final = sign_one_md5.hexdigest().upper()

    url = bind_phone_url + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + \
        "&language=" + language + "&timestamp=" + \
        str(calendar.timegm(time.gmtime())) + \
        "&token=" + get_login_token() + "&userid=" + get_login_userid()

    req = requests.get(url, headers={"User-Agent": header_str})
    req_txt = req.text
    req_json = json.loads(req_txt)
    print(req_txt)
    if req_json['error'] == 0:
        text = req_json['data']['text']
        print(text)
    else:
        print(req_txt)


def input_ref_code():
    global ref_code
    while True:
        try:
            ref_code = str(input("Enter referral code: "))
            if not ref_code:
                continue
            elif ref_code.isdigit() and len(ref_code) == 7:    
                f = open("config.txt", "a")
                f.write("Ref Code: " + ref_code + "\n")
                break
        except ValueError as e:
            print(e)
    
def bind_code():
    url = bind_code_url + "token=" + get_login_token() + "&app_version=" + app_version + \
        "&language=" + language + "&device_string=" + device_string + "&code=" + ref_code
    req = requests.get(url, headers={"User-Agent": invite_header})
    req_txt = req.text
    req_json = json.loads(req_txt)
    if req_json['error'] == 0:
        coins = req_json['data']['text']
        print(coins)
    else:
        print(req_txt)

def menu():
    print("SM-HOME by @pigscanfly")
    print("[1] Sign-up")
    print("[2] Refer Code")
    choice = str(input("Enter #: "))

    if choice == "1":
        set_filename()
        get_token()
        input_mobile()
        send_code()
        input_code()
        login()
    elif choice == "2":    
        bind_phone()
        # input_ref_code()
        # bind_code()

menu()        
