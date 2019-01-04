import os
import sys
import ast
import json
import glob
import tweepy
import dateutil.parser
import zipfile
import tempfile

class twelete:

        # private variables
        #----------------------------------------------------------------------------
        api_key_set = False
        access_token_set = False

        
        filter_date = False
        filter_activity = False
        filter_media = False

        
        filter_phrase_black = False
        filter_phrase_white = False

        
        # variable selection
        # ---------------------------------------------------------------------------           
        def set_api_key(self, api_key, api_key_secret):
                twelete.api_key_set = True
                self.api_key=api_key
                self.api_key_secret=api_key_secret


        def set_access_tokens(self, access_token, access_token_secret):
                twelete.access_token_set = True
                self.access_token=access_token
                self.access_token_secret=access_token_secret
                

        def set_date_filter(self, x, y):
                twelete.filter_date = True
                self.date_min=dateutil.parser.parse(str(x + " 00:00:00 +0000"))
                self.date_max=dateutil.parser.parse(str(y + " 00:00:00 +0000"))


        def set_activity_filter(self, x, y):
                twelete.filter_activity = True
                self.rt_min=x
                self.like_min=y
                

        def set_media_filter(self, x):
                twelete.filter_media = True
                self.media_filter = x


        def set_phrase_blacklist_filter(self, x):
                twelete.filter_phrase_black = True
                for a in x:
                        self.phrase_list_black.append(a)


        def set_phrase_whitelist_filter(self, x):
                twelete.filter_phrase_white = True
                for a in x:
                        self.phrase_list_white.append(a)

                
        def set_keybase_twitter(self,x):
                a = "Verifying myself: I am " + x + " on http://Keybase.io ."
                self.set_phrase_whitelist_filter([a])
                




        # Error handler
        #----------------------------------------------------------------------------
        def log_handle(self, log, log_file):
                print(log)
                with open(log_file, "a") as x:
                    x.write(log + "\n")
           

        def log_notify(self, notif):
                self.log_handle(str("[INFO]: "+notif),self.notify_log_file)


        def log_warn(self, warn):
                self.log_handle(str("[WARNING]: "+warn),self.warn_log_file)


        def log_err(self, err):
                self.log_handle(str("[ERROR]: "+err),self.err_log_file)
                sys.exit()


        def err_tweepy(self, err):
                # format dodgy returns from tweepy api
                err_dict_list = ast.literal_eval(err.response.text)

                # print errors
                for x in err_dict_list['errors']:
                        if x['code'] in [215]:
                                self.log_err(str("{} ({})").format(x['message'], x['code']))
                        elif x['code'] in [88]:
                                
                                self.log_warn(str("{} ({})").format(x['message'], x['code']))
                                self.log_notify("Retrying..")
                                return True
                        else:
                                self.log_warn(str("{} ({})").format(x['message'], x['code']))




        # runtime requirement fetching
        # ---------------------------------------------------------------------------
        def get_query(self, request):
                self.log_notify(request)
                while True:
                        try:
                                response = input("> ")
                                if response in ("y","Y"):
                                        return True
                                elif response in ("n","N"):
                                        return False
                                else:
                                        raise ValueError()
                        except ValueError:
                                self.log_warn("Please enter \"Y\" or \"N\"")


        def get_num(self, request):
                self.log_notify(request)
                while True:
                        try:
                                response = input("> ")
                                response = int(response)
                                return response
                        except ValueError:
                                self.log_warn("Please enter a base 10 number.")  


        def get_date(self, request):
                self.log_notify(request)
                while True:
                        try:
                                response = input("> ")
                                response = str(response + " 00:00:00 +0000")
                                date = dateutil.parser.parse(response)
                                return date
                        except ValueError:
                                self.log_warn("Please enter a valid yyyy-mm-dd date.")


        def get_string(self, request, not_empty):
                self.log_notify(request)
                while True:
                        try:
                                response = input("> ")
                                if response in ("", " "):       
                                        if not_empty:
                                                raise ValueError()
                                        else:
                                                return False
                                return response
                        except ValueError:
                                self.log_warn("Please enter a value")


        def get_archive_dir(self):
                self.log_notify("Please enter the path to your twitter .zip archive")
                while True:
                        try:
                                response = input("> ")
                                if os.path.isfile(response) == False:
                                        raise FileNotFoundError()
                                if zipfile.is_zipfile(response) == False:
                                        raise zipfile.BadZipFile()
                                return response
                        except zipfile.BadZipFile:
                                self.log_warn(str("\"{}\" is not a zip file!").format(response))
                        except FileNotFoundError:
                                self.log_warn(str("cannot find file \"{}\"").format(response))
                        except PermissionError:
                                self.log_warn(str("cannot open \"{}\" (invalid permsisions).").format(response))


        def get_api_tokens(self):
                self.set_api_key(
                        self.get_string("Please enter your API Key", True),
                        self.get_string("Please enter your API Key Secret", True))

                self.set_access_tokens(
                        self.get_string("Please enter your Access Token", False),
                        self.get_string("Please enter your Access Token Secret", False))


        def get_filters(self):
                if self.get_query("Filter based on date? (Y/N):"):
                       self.set_date_filter(
                               self.get_date("Please enter a date lower bound (yyyy-mm-dd)"),
                               self.get_date("Please enter a date upper bound (yyyy-mm-dd)"))

                if self.get_query("Filter based on minimum activity? (Y/N):"):
                       self.set_activity_filter(
                                self.get_num("Please enter the minimum retweet requirement"),
                                self.get_num("Please enter the minimum like requirement"))
                
                if self.get_query("Filter based on media contents (Y/N):"):
                        while True:
                                response = self.get_string("delete tweets WITH media or delete tweets WITHOUT media? (WITH/WITHOUT)\n", True)
                                if response.lower() == "with":
                                        self.set_media_filter(True)
                                        break
                                elif response.lower() == "without":
                                        self.set_media_filter(False)
                                        break

                if self.get_query("blacklist phrases in text? (Y/N):"):
                        filter_list = []
                        while True:
                                response = self.get_string("enter string to filter by; Press enter to finish entering.", False)
                                if response == False:
                                        break
                                else:
                                        filter_list.append(response)
                        self.set_phrase_blacklist_filter(filter_list)

                if self.get_query("whitelist phrases in text? (Y/N):"):
                        filter_list = []
                        while True:
                                response = self.get_string("enter string to filter by; Press enter to finish entering.", False)
                                if response == False:
                                        break
                                else:
                                        filter_list.append(response)
                        self.set_phrase_whitelist_filter(filter_list)
                        
                if self.get_query("preserve keybase proof? (Y/N):"):
                        response = self.get_string("please enter your keybase username.", True)
                        self.set_keybase_twitter(response)

                                
        def get_confirm(self):
                print("-----------------------------------")
                self.log_notify(str("Archive directory: {}").format(self.archive_dir))

                if self.filter_date:
                        self.log_notify(
                                str("Tweet date range is \n    After  {}\n    Before {}").format(
                                        self.date_min.isoformat(), self.date_max.isoformat()))

                if self.filter_activity:
                        self.log_notify(str("Tweets with less than {} retweets will be deleted").format(self.rt_min))
                        self.log_notify(str("Tweets with less than {} likes will be deleted").format(self.like_min))

                print("-----------------------------------")
                response = self.get_query("Do you wish to continue? (y/n)")
                return response




        # archive management
        # ---------------------------------------------------------------------------
        def read_file(self, file_name):
                self.log_notify(str("loading {}").format(file_name))
                f = open(file_name, 'r', encoding='utf8')
                # clear the first junk line
                f.readline() 
                data = json.load(f);
                data.sort(key=lambda x: x['created_at'])
                return data


        def load_js(self):
                self.log_notify("fetching tweets from excracted archive..")
                self.file_list = glob.glob(str(self.extract_dir) + "/data/js/tweets/*.js")
                if self.file_list == []:
                        self.log_err("No js files found in extracted tweet archive")
                else:
                        self.file_list.sort()
                        self.log_notify("..Done.")


        def unzip_archive(self):
                self.log_notify("fetching tweet archive from \"{}\"..".format(self.archive_dir))
                try:
                        if os.path.isfile(self.archive_dir) == False:
                                        raise FileNotFoundError()
                        if zipfile.is_zipfile(self.archive_dir) == False:
                                raise zipfile.BadZipFile()
                        with zipfile.ZipFile(self.archive_dir) as zf:
                                zf.extractall(self.extract_dir)
                except zipfile.BadZipFile:
                        self.log_err(str("\"{}\" is not a zip file!").format(self.archive_dir))
                except FileNotFoundError:
                        self.log_err("cannot locate twitter archive.")




        # prerequisites
        # ---------------------------------------------------------------------------
        def fetch_archive(self):
                self.extract_dir = os.path.splitext(self.archive_dir)[0]
                self.unzip_archive()
                self.load_js()


        def fetch_api(self):
                self.log_notify("Loading api..")
                if twelete.api_key_set:    
                        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
                else:
                        self.log_err("No api key set")

                if twelete.access_token_set:     
                        auth.set_access_token(self.access_token, self.access_token_secret)
                else:
                        self.log_warn("no access token set")          

                self.api = tweepy.API(auth)
                self.log_notify("..api loaded.")
        



        # filter checks
        # ---------------------------------------------------------------------------
        def check_date(self, tweet):
                # check date boundaries of status
                if self.filter_date:
                        tweet_date = dateutil.parser.parse(tweet['created_at'])
                        if tweet_date < self.date_min:
                                return True
                        if tweet_date > self.date_max:
                                return True
                return False

        
        def check_activity(self):
                # check activity boundaries of status
                # [NOTE]: favorites mean the same as likes, just twitter legacy.
                if self.filter_activity:
                        if self.status.retweet_count >= self.rt_min:
                                return True
                        if self.status.favorite_count >= self.like_min:
                                return True
                return False

        
        def check_media(self, tweet):
                # check if status contains media
                if self.filter_media:
                        if tweet['entities']['media'] != []:
                                return self.media_filter
                        else:
                                return not self.media_filter
                return False


        def check_phrase_black(self, tweet):
                # check if status contains blacklisted phrase
                text =  tweet['text']       
                if self.filter_phrase_black:
                        for x in self.phrase_list_black:
                                if x in text:
                                        self.log_notify("Found blacklisted phrase {}.".format(x))
                                        return False
                        return True
                return False


        def check_phrase_white(self, tweet):
                # check if status contains whitelisted phrase
                text =  tweet['text']       
                if self.filter_phrase_white:
                        for x in self.phrase_check:
                                if x in text:
                                        self.log_notify("Found whitelisted phrase {}.".format(x))
                                        return True
                return False



        
        # tweet deletion
        # ---------------------------------------------------------------------------
        def status_info(self, tweet):
                try:
                        print(tweet['text'])
                except UnicodeEncodeError:
                        log_warn("unprintable unicode in tweet")


        def fetch_status(self, tweet):
                # try to fetch status from twitter
                while True:
                        try:
                                self.status = self.api.get_status(tweet['id'])
                                return False
                        except tweepy.TweepError as e:
                                if not self.err_tweepy(e):
                                        break
                return True
                
        
        def commit_delete(self, tweet):
                while True:
                        try:
                                #self.api.destroy_status(tweet['id'])
                                self.log_notify("Deleted tweet " + str(tweet['id']))
                                break
                        except tweepy.TweepError as e:
                                 if not self.err_tweepy(e):
                                        break

             
        def delete_tweets(self):
                self.fetch_archive()
                self.fetch_api()
                for file_name in self.file_list:
                        data = self.read_file(file_name)
                        for tweet in data:
                                if self.check_date(tweet):
                                        continue
                                if self.fetch_status(tweet):
                                        continue
                                if self.check_activity():
                                        continue
                                if self.check_media(tweet):
                                        continue
                                if self.check_phrase_black(tweet):
                                        continue
                                if self.check_phrase_white(tweet):
                                        continue
                                
                                self.status_info(tweet)
                                self.commit_delete(tweet)
                                print("-----------------------------------")
                                
                                


        # main
        # ---------------------------------------------------------------------------       
        def run(self):
                self.get_api_tokens()
                self.get_filters()
                self.archive_dir=self.get_archive_dir()
                confirm_delete = self.get_confirm()
                
                if confirm_delete:
                        self.delete_tweets()
                        self.log_notify("Tweets deleted. Exiting...")
                else:
                        self.log_notify("No tweets deleted. Exiting...")
                sys.exit()

                
        def __init__(self):
                # date filters
                self.date_min = int()
                self.date_max = int()

                # activity filters
                self.rt_min = int()
                self.like_min = int()

                # media filter
                # True = delete with | False = delete without
                self.media_filter = bool()

                # tweet phrase filters
                self.phrase_list_black = []
                self.phrase_list_white = []


                # directory of twitter archive
                self.archive_dir = ""

                # api keys
                self.api_key ="XXXXXXXXX"
                self.api_key_secret = "XXXXXXXXX"   
                self.access_token = "XXXXXXXXX"    
                self.access_token_secret = "XXXXXXXXX"

                #log files
                self.notify_log_file = "./twelete.log"
                self.warn_log_file = "./twelete.log"
                self.err_log_file = "./twelete.log"

