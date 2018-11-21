import Twelete

api_key="XXXXXXXXXXXXXXXXXXx"
api_key_secret="XXXXXXXXXXXXXXXXXXx"

access_token="XXXXXXXXXXXXXXXXXXx-XXXXXXXXXXXXXXXXXXx"
access_token_secret="XXXXXXXXXXXXXXXXXXx"

archive_dir ="/path/to/archive"
date_min="2016-01-24"
date_max="2019"

rt_min=-1
likes_min=-1

word_list= [" test "," me "]

def main():
    app = Twelete.twelete()
    app.archive_dir=archive_dir

    # connect to twitter API
    app.set_api_key(api_key,api_key_secret)
    app.set_access_tokens(access_token, access_token_secret)

    #app.set_media_filter(True)
    #app.set_date_filter(date_min, date_max)
    #app.set_activity_filter(rt_min, likes_min)
    #app.set_phrase_filter(word_list)
    app.delete_tweets()
    
if __name__ == '__main__':main()

    
