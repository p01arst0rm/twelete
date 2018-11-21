Twelete
===========

Twitter status removal tool for python 3.7. This tool is a heavily 
modified version of a tool by sjtrny. Original is available 
[here](https://github.com/sjtrny/TweetDelete/blob/master/delete_tweets.py).

Dependencies
-----------

- tweepy 
	- git+https://github.com/tweepy/tweepy.git 
	- be sure to use this version; other versions may cause errors in python >=3.7
	- see http://www.tweepy.org for more information
- glob
	- glob3
- dateutil
	- python-dateutil
	
User Guide
-----------

1. Download your [Twitter archive](https://twitter.com/settings/account)
- Install dependencies
	- `pip install git+https://github.com/tweepy/tweepy.git`
	- `pip install glob3`
	- `pip install python-dateutil`
- Make a developer account at [dev.twitter.com](http://dev.twitter.com)
- Create a new twitter app
- Set app permissions to read and write
- Generate access token for your app
- clone repository
- execute run_interactive.py
- follow instructions given