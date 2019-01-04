import Twelete

api_key="XXXXXXXXXXXXXXXXXXXXXXX"
api_key_secret="XXXXXXXXXXXXXXXXXXXXXXX"

access_token="XXXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret="XXXXXXXXXXXXXXXXXXXXXXX"

archive_dir ="/path/to/archive.zip"
date_min="2016-01-24"
date_max="2019"

rt_min=-1
likes_min=-1

twitter_username = "dril"
whitelist= [" save "," me "]
blacklist= [" kill "," me "]

def main():
    app = Twelete.twelete()
    app.archive_dir=archive_dir

    # connect to twitter API
    app.set_api_key(api_key,api_key_secret)
    app.set_access_tokens(access_token, access_token_secret)

    #app.set_media_filter(True)
    #app.set_date_filter(date_min, date_max)
    #app.set_activity_filter(rt_min, likes_min)
    #app.set_keybase_twitter(twitter_username)
    #app.set_phrase_whitelist_filter(whitelist)
    #app.set_phrase_blacklist_filter(blacklist)
    app.delete_tweets()
    
if __name__ == '__main__':main()

    
