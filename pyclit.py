#!/usr/bin/env python

import json, tweepy, sys, os
from getopt import *

def horizontalLines(count = 1, ch = '-'):
  # Get size of console
  rows, columns = os.popen('stty size', 'r').read().split()
  print ( ch * int( int(columns) / len(ch) ) + '\n' ) * count,

def printTweets(tweetsList):
  horizontalLines()
  for message in tweetsList: 
    print message.user.name + ' - @' + message.user.screen_name
    print message.text
    print '  > ' + str(message.created_at) + ' via ' + message.source
    horizontalLines()

def pyclit(auth=False, tweet=None, home=False, mention=False, dm=False, interactive=False):
  consumer_key = 'C0KI0nXR4BQizZdWYFSBQ'
  consumer_secret = 'f6lI5yGxXl8cdYVAO1fdHm69M6vtN5wKM7UCG5b0xY'

  if auth:
    print "Login process:"
    au = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
      authorization_url = au.get_authorization_url()
    except tweepy.TweepError:
      print 'Faild to get request token.'
      return
    print "Now get verifier code from the following url:"
    print "Authorization URL: " + authorization_url 

    verifier = raw_input('Verifier Code:')
    try:
      au.get_access_token(verifier)
    except tweepy.TweepError:
      print 'Faild to get access token.'
      return

    try:
      fp = open('.pyclitrc', 'w')
      profile = {
        'key': au.access_token.key,
        'secret': au.access_token.secret
      }
      json.dump(profile, fp)
      fp.close()
    except IOError:
      print 'Faild to save access token.'
      return

  try:
    fp = open('.pyclitrc', 'r')
    profile = json.load(fp)
  except IOError:
    print "Cannot open authorized account, please use --auth to login."
    return

  try:
    au = tweepy.OAuthHandler(consumer_key, consumer_secret)
    au.set_access_token(profile['key'], profile['secret'])
    api = tweepy.API(au)
  except tweepy.TweepError:
    print "Faild in Authorization, you may try to use --auth to relogin."

  if tweet is not None:
    api.update_status(tweet)

  if home == True:
    print 'Home:'
    printTweets(reversed(api.home_timeline()))

if __name__ == '__main__':
  manual = '''pyclit.py - commandline based lightweight twitter client.

  options:
    --auth                      Authorization account.
    -s=<msg>, --tweet=<msg>     Send tweet.
    -t, --home                  Get tweets from home timeline.
    -m, --mentions              Get mentions.
    -d, --dm                    Get Direct Messages.
    -i, --interactive           Interactive Mode.
'''
  try:
    opts, args = getopt( sys.argv[1:], 'ts:h', [ 'home', 'tweet=', 'help', 'auth' ] )
  except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)

  #Defaults
  home = False
  auth = False
  tweet = None
  help = False
  
  for o, a in opts:
    if o in ('-t','--home'):
      home = True
    elif o in ('-s','--tweet'):
      tweet = a
    elif o in ('-h', '--help'):
      help = True
    elif o == '--auth':
      auth = True

  if help:
    print manual
    sys.exit(0)
  
  pyclit(auth, tweet, home)
