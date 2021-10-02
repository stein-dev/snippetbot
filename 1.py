import hashlib
import requests
import json
import calendar
import datetime
import time

userid = "1720339"
token_file = "1.txt"
device_string = "Android:7.0:Redmi Note 4:[si1=1080x1920,3.0]:541091e4b39864dd"

header_str = "Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36"
mall_header = "Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/OPM7.181105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.109 Mobile Safari/537.36 SnippetMedia_Android"

app_version = "3.4.5"
language = "en"
cycle_num = "1"
limit_seconds = "30"
reward_count = "1"
release_key = "u5kC9lODPmeHW2KbzCWCI9BlO4xHrxo4"
num = 0
limit = "10"
cat_arr_news = ["ForU", "Gaming", "Tech", "Sports", "Travel", "Biz", "Anime", "Lifestyle", "Music", "News", "Motor", "Tagalog", "Pet", "Kpop", "Entertain", "Food", "Fashion", "Health"]
cat_arr_video = ["Videos", "Video_Sport", "Video_Anime", "Video_Game", "Video_Tech", "Video_News", "Video_Kpop", "Video_Pet", "Video_Entertainment", "Video_Travel", "Video_Life", "Video_Tech", "Video_Society"]
ntype = "top"
nremaing_id = 2
counter = 0
currentDT = datetime.datetime.now()
platform = "Twitter"
delay = 30

api_listing_news = "http://release-sg-api.snippetmedia.com/listing?"
api_listing_video = "http://release-sg-api.snippetmedia.com/listing/videos?"
api_method_news = "http://release-sg-api.snippetmedia.com/UserReadAward/read?"
api_method_video = "http://release-sg-api.snippetmedia.com/UserReadAward/view?"
api_like = "http://release-sg-api.snippetmedia.com/EverydayTask/like_new?"
api_share = "http://release-sg-api.snippetmedia.com/EverydayTask/share_new?"
api_score = "http://release-sg-api.snippetmedia.com/User/score?"
api_signin = "http://release-sg-api.snippetmedia.com/TaskSignIn/active?"
api_openbox = "http://release-sg-api.snippetmedia.com/SpUserKbbx/add_open_bbx?"
api_time_openbox = "http://release-sg-api.snippetmedia.com/SpUserKbbx/get_recently_open_bbx_time?"
api_qrcode = "http://release-sg-api.snippetmedia.com/SpShareActivity/sharing_qr_code?"
api_emoney = "http://release-sg-api.snippetmedia.com/Cash/remaining_count?"
api_load = "http://release-sg-api.snippetmedia.com/Product?"
api_withdraw = "http://release-sg-api.snippetmedia.com/Cash/withdrawal?"
api_refresh = "http://release-sg-api.snippetmedia.com/Token/refresh_token?"
api_refer = "http://release-sg-api.snippetmedia.com/MentoringActivity/inviter_detail?"
api_userinfo = "http://release-sg-api.snippetmedia.com/User/info?"


CYELLOW = '\033[93m'
CGREEN = '\33[32m'
CEND = '\033[0m'
    
def get_token():
    try:
        f = open(token_file, "r")
        token = str(f.readline())
        return token
    except FileNotFoundError as e:
        print(e)    
    finally:
        f.close()       

def is_token_expired(): 
    try:
        score_url = api_score + "token=" + get_token() + "&app_version=" + app_version + "&language=" + language + "&device_string=" + device_string    
        score_r = requests.get(score_url, headers={"User-Agent": mall_header})
        score_str1 = score_r.text
        score_str2 = json.loads(score_str1)
        error_str = score_str2['error']
        if error_str == 120:
            return True
        else:
            return False   
    except ValueError as e:
        print(e)     

def token_refresh():
    try:
        timestamp = calendar.timegm(time.gmtime())
        sign_one = app_version + device_string + language + str(timestamp) + get_token() + userid + release_key
        sign_one_md5 = hashlib.md5(sign_one.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()

        url = api_refresh + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&userid=" + userid

        req = requests.get(url, headers={"User-Agent": header_str})
        req_txt = req.text
        req_json = json.loads(req_txt)
        error_str2 = req_json['error']
        if error_str2 == 0:
            new_token = str(req_json['data']['token'])
            return new_token  
    except ValueError as e:
        print(e)        

def save_token():
    try:
        ntoken = token_refresh()
        if not ntoken:
            print("No token received.")
        else:
            print("New Token:", ntoken)
            try:
                f = open(token_file, "w")
                f.write(str(ntoken))
            except FileNotFoundError  as e:
                print(e)    
            finally:
                f.close() 
    except ValueError as e:
        print(e)                        

def read_news():
    for sec in cat_arr_news:
        try:
            timestamp = calendar.timegm(time.gmtime())
            sign_one_str = app_version + device_string + language + limit + sec + str(timestamp) + get_token() + ntype + userid + release_key
            sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
            sign_one_final = sign_one_md5.hexdigest().upper()

            listing_news = api_listing_news + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&limit=" + limit + "&section=cat:" + sec + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&type=" + ntype + "&userid=" + userid

            listing_news_r = requests.get(listing_news, headers={"User-Agent": header_str})
            listing_news_str1 = listing_news_r.text
            listing_news_str2 = json.loads(listing_news_str1)
            for ids in listing_news_str2['data']['news_list']:
                timestamp = calendar.timegm(time.gmtime())

                sign_two_str = reward_count + ids["nid"] + release_key 
                sign_two_md5 = hashlib.md5(sign_two_str.encode("utf-8"))
                sign_two_final = sign_two_md5.hexdigest().upper()

                sign_one_str = app_version + cycle_num + device_string + ids["nid"] + language + limit_seconds + sign_two_final + str(timestamp) + get_token() + userid + release_key
                sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
                sign_one_final = sign_one_md5.hexdigest().upper()

                news_url = api_method_news + "_sign=" + sign_one_final + "&app_version=" + app_version + "&cycle_num=" + cycle_num + "&device_string=" + device_string + "&id=" + ids["nid"] + "&language=" + language + "&limit_seconds=" + limit_seconds + "&sign=" + sign_two_final + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&userid=" + userid

                read_r = requests.get(news_url, headers={"User-Agent": header_str})
                read_str1 = read_r.text
                read_str2 = json.loads(read_str1)
                error_str = read_str2['error']
                if error_str == 0:
                    coin_str = read_str2['data']['text']
                    print(CGREEN + "News -> " + coin_str + CEND)
                    time.sleep(delay)   
                else:
                    error_msg = read_str2['data']['message']
                    print(CYELLOW + "News -> " + error_msg + CEND)
                    time.sleep(delay)
                    continue       
        except ValueError as e:
            print(e)
            continue    

def watch_video():
    for sec in cat_arr_video:
        try:
            timestamp = calendar.timegm(time.gmtime())
            sign_one_str = app_version + device_string + language + limit + sec + str(timestamp) + get_token() + ntype + userid + release_key
            sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
            sign_one_final = sign_one_md5.hexdigest().upper()
            listing_video = api_listing_video + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&limit=" + limit + "&section=cat:" + sec + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&type=" + ntype + "&userid=" + userid
            listing_video_r = requests.get(listing_video, headers={"User-Agent": header_str})
            listing_video_str1 = listing_video_r.text
            listing_video_str2 = json.loads(listing_video_str1)
            for ids in listing_video_str2['data']['news_list']:
                
                sign_two_str = reward_count + ids["nid"] + release_key 
                sign_two_md5 = hashlib.md5(sign_two_str.encode("utf-8"))
                sign_two_final = sign_two_md5.hexdigest().upper()

                sign_one_str = app_version + cycle_num + device_string + ids["nid"] + language + limit_seconds + sign_two_final + str(timestamp) + get_token() + userid + release_key
                sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
                sign_one_final = sign_one_md5.hexdigest().upper()

                video_url = api_method_video + "_sign=" + sign_one_final + "&app_version=" + app_version + "&cycle_num=" + cycle_num + "&device_string=" + device_string + "&id=" + ids["nid"] + "&language=" + language + "&limit_seconds=" + limit_seconds + "&sign=" + sign_two_final + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&userid=" + userid

                read_r = requests.get(video_url, headers={"User-Agent": header_str})
                read_str1 = read_r.text
                read_str2 = json.loads(read_str1)
                error_str = read_str2['error']
                if error_str == 0:
                    coin_str = read_str2['data']['text']
                    print(CGREEN + "Video -> " + coin_str + CEND)
                    time.sleep(delay)
                else:
                    error_msg = read_str2['data']['message']
                    print(CYELLOW + "Video -> " +  error_msg + CEND)
                    time.sleep(delay)
                    continue   
        except ValueError as e:
            print(e)     
            continue  

def like():
    try:
        timestamp = calendar.timegm(time.gmtime())
        sign_one_str = app_version + device_string + language + limit + "cat:ForU" + str(timestamp) + get_token() + ntype + userid + release_key
        sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()

        listing_news = api_listing_news + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&limit=" + limit + "&section=cat:ForU"  + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&type=" + ntype + "&userid=" + userid

        listing_news_r = requests.get(listing_news, headers={"User-Agent": header_str})
        listing_news_str1 = listing_news_r.text
        listing_news_str2 = json.loads(listing_news_str1)
        for ids in listing_news_str2['data']['news_list']:
            sign_one_str = app_version + device_string + ids["nid"] + language + str(timestamp) + get_token() + userid + release_key
            sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
            sign_one_final = sign_one_md5.hexdigest().upper()

            like_url = api_like + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&id=" + ids["nid"] + "&language=" + language + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&userid=" + userid    
            
            read_r = requests.get(like_url, headers={"User-Agent": header_str})
            read_str1 = read_r.text
            read_str2 = json.loads(read_str1)
            error_str = read_str2['error']
            if error_str == 0:
                coin_str = read_str2['data']['text']
                print(CGREEN + "Like -> " + coin_str + CEND)
                time.sleep(2)
            else:
                error_msg = read_str2['data']['message']
                print(CYELLOW + "Like -> " + error_msg + CEND)
                time.sleep(2)
                break
    except ValueError as e:
        print(e) 

def share():
    try:
        timestamp = calendar.timegm(time.gmtime())
        sign_one_str = app_version + device_string + language + limit + "cat:ForU" + str(timestamp) + get_token() + ntype + userid + release_key
        sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()

        listing_news = api_listing_news + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&limit=" + limit + "&section=cat:News" + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&type=" + ntype + "&userid=" + userid

        listing_news_r = requests.get(listing_news, headers={"User-Agent": header_str})
        listing_news_str1 = listing_news_r.text
        listing_news_str2 = json.loads(listing_news_str1)
        for ids in listing_news_str2['data']['news_list']:
            sign_one_str = app_version + device_string + ids["nid"] + language + str(timestamp) + get_token() + userid + release_key
            sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
            sign_one_final = sign_one_md5.hexdigest().upper()

            share_url = api_share + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&id=" + ids["nid"] + "&language=" + language + "&timestamp=" + str(timestamp) + "&token=" + get_token() + "&userid=" + userid    
            
            read_r = requests.get(share_url, headers={"User-Agent": header_str})
            read_str1 = read_r.text
            read_str2 = json.loads(read_str1)
            error_str = read_str2['error']
            if error_str == 0:
                coin_str = read_str2['data']['text']
                print(CGREEN + "Share -> " + coin_str + CEND)
                time.sleep(2)
            else:
                error_msg = read_str2['data']['message']
                print(CYELLOW + "Share -> " + error_msg + CEND)
                time.sleep(2)
                break
    except ValueError as e:
        print(e)

def qrcode():
    try:
        timestamp = calendar.timegm(time.gmtime())
        sign_one_str = app_version + device_string + language + platform + str(timestamp) + get_token() + userid + release_key
        sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()

        qrcode_url = api_qrcode + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&platform=" + platform + "&timestamp=" + str(timestamp) + "&token=" + get_token()  + "&userid=" + userid
        qrcode_r = requests.get(qrcode_url, headers={"User-Agent": header_str})
        qrcode_str1 = qrcode_r.text
        qrcode_str2 = json.loads(qrcode_str1)
        error_str = qrcode_str2['error']
        if error_str == 0:
            qrcode_reward = qrcode_str2['data']['text']
            print(CGREEN + "QR -> " + qrcode_reward + CEND)
        else:
            print(CYELLOW + "QR -> Already Shared" + CEND)
    except ValueError as e:
        print(e)  

def chest():
    try:
        timestamp = calendar.timegm(time.gmtime())
        sign_one_str = app_version  + device_string + language + str(timestamp) + get_token() + release_key
        sign_one_md5 = hashlib.md5(sign_one_str.encode("utf-8"))
        sign_one_final = sign_one_md5.hexdigest().upper()
        openbox_url = api_openbox + "_sign=" + sign_one_final + "&app_version=" + app_version + "&device_string=" + device_string + "&language=" + language + "&timestamp=" + str(timestamp) + "&token=" + get_token()
        openbox_r = requests.get(openbox_url, headers={"User-Agent": header_str})
        openbox_str1 = openbox_r.text
        openbox_str2 = json.loads(openbox_str1)
        error_str = openbox_str2['error']
        if error_str == 0:
            openbox_reward = openbox_str2['data']['text']
            print(CGREEN + "Chest -> " + openbox_reward + CEND)
        else:
            print(CYELLOW + "Chest -> Time Insufficient" + CEND)   
    except ValueError as e:
        print(e)

while True:
    if is_token_expired() == True:
        save_token()
    else:    
        qrcode()
        chest()
        like()
        share() 
        read_news()
        chest()
        watch_video()   
        chest()