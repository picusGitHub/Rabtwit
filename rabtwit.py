#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Name: Rabtwit (v.0.2.0)
# About: hashtag hijacking tool in Python. It sends tweets with the link of a random rabbit image from Google and with random tags from a file. 
#        Let's hijack them with those cute bunnies <3
#        Please customize the hashtags.txt and searchterms.txt files
# Warning: for security reasons, do not use this tool with your personal Twitter account
# Credit: picus & all the white rabbits out there
#            ,
#            /|      __
#           / |   ,-~ /
#          Y :|  //  /
#          | jj /( .^
#          >-"~"-v"
#         /       Y
#        jo  o    |
#       ( ~T~     j
#        >._-' _./
#       /   "~"  |
#      Y     _,  |
#     /| ;-"~ _  l
#    / l/ ,-"~    \
#    \//\/      .- \
#     Y        /    Y    -Row
#     l       I     !
#     ]\      _\    /"\
#    (" ~----( ~   Y.  )
#~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# Requirements:
# - Python 2.7
# - Python Requests Module (http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests)
# - Simplejson (https://pypi.python.org/pypi/simplejson)
#  
# 
# Usage:  python rabtwit.py -u <Twitter username>  [--tmin=<min minutes between tweets> --tmax=<max minutes between tweets>]
# Example: the command "python rabtwit.py -u exampleuser --tmin=7 --tmax=13" will tweet a rabbit every 7 to 13 minutes
#           
# Linux/Unix:
# - Linux Pip install instructions: http://pip.readthedocs.org/en/stable/installing/
# - Requests module instructions: http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests (pip install requests) (pip install request[security])
# 
# Windows:
# - Make sure pip is installed: http://pip.readthedocs.org/en/stable/installing/
# - Open up cmd and run c:\python27\scripts\easy_install.exe request
# 
# Need Help or Find a Bug?
# - /join #OpParis-Dev - https://webchat.anonops.com/?channels=OpParis-Dev and contact picus or any other rabbit
# 

import sys, time, getopt, getpass, random
import simplejson as json
from lxml.html import fromstring
try:
	import requests
except:
    print "Please install the requests module."
    print "* Unix/Linux Use: pip install requests"
    print "* Windows in CMD: c:\python27\scripts\easy_install.exe request"
    print "* More Info: http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests"
    sys.exit()

VERSION = "v 0.2.0"
HASHTAGS_FILE="hashtags.txt"
SEARCHTERMS_FILE="searchterms.txt"
RABBIT="rabbit_art.txt"
BUNNY_HASHTAG="#rabtwit"
DEFAULT_MIN_TIME=5
DEFAULT_MAX_TIME=10

def main(argv):
    username = None
    boot_screen="\n*******************************************************\n"
    boot_screen+="*                   RabTwit "+VERSION+"                   *\n"                                   
    boot_screen+="*         Let's flood twitter with cute bunnies!      *\n"
    boot_screen+="*******************************************************"	
    usageString = boot_screen+"\nUsage: python rabtwit.py -u <Twitter username>  [--tmin=<min minutes between tweets> --tmax=<max minutes between tweets>]\n       If not specified, <min time between tweets> is set to 5, <max time between tweets> is set to 10.\n"
    try:
        opts, args = getopt.getopt(argv,"h:u:",["user=","tmin=","tmax="])
    except getopt.GetoptError:
        print usageString
        sys.exit(2)

    minTime=None
    maxTime=None

    for opt, arg in opts:
        if opt == '-h':
            print usageString
            sys.exit()
        elif opt in ("-u", "--user"):
            username = arg
	elif opt == "--tmin":	
	    minTime=arg
	elif opt == "--tmax":
	    maxTime=arg

    #A few checks
    if not username:
        print usageString
        sys.exit()
    if ((not minTime) and (not maxTime)):
	minTime=DEFAULT_MIN_TIME
	maxTime=DEFAULT_MAX_TIME
    elif (minTime and (not maxTime)) or ((not minTime) and maxTime):
	print usageString+"\nError: you specified only one of options <min time between tweets> and <max time between tweets>"
	sys.exit()
    elif (not minTime.isdigit()) or (not maxTime.isdigit()):
	print usageString+"\nError: <min time between tweets> and <max time between tweets> must be integer"
	sys.exit()
    elif (int(minTime)>int(maxTime)):
	print usageString+"\nError: <min time between tweets> must be lower than <max time between tweets>"
	sys.exit()

    #Print the ASCII Rabbit
    print boot_screen
    f=open(RABBIT,'r')
    print f.read()
    f.close()

    password = getpass.getpass()

# uncomment this section if you want to use privoxy + tor:
#    proxyIP = '127.0.0.1'
#    proxyPort = 8118
#
#    proxy_settings = {'network.proxy.type': 1,
#            'network.proxy.http': proxyIP,
#            'network.proxy.http_port': proxyPort,
#            'network.proxy.ssl': proxyIP,
#            'network.proxy.ssl_port':proxyPort,
#            'network.proxy.socks': proxyIP,
#            'network.proxy.socks_port':proxyPort,
#            'network.proxy.ftp': proxyIP,
#            'network.proxy.ftp_port':proxyPort 
#            }
#
    try:
	print "Connecting to twitter..."
	bot = requests.Session()
	url = 'https://mobile.twitter.com/session'
        response = bot.get(url)
   
        html = fromstring(response.content)
        payload = dict(html.forms[0].fields)
        payload.update({'username': username,'password': password,})
 	login=bot.post(url, data=payload)
	
	if "https://mobile.twitter.com/login/error" in login.url:
        	print "Twitter login Failed!"
                sys.exit()

    except Exception,e:
    	print "Unexpected error occured while trying the Twitter login. Please try running the script again."
	print e
        sys.exit()

    print "Twitter login done!"

    try:
	hashtags=open(HASHTAGS_FILE).read().splitlines()
    	search_terms=open(SEARCHTERMS_FILE).read().splitlines()
    except:
	print "Error while opening the hashtags and searchterms files."
	sys.exit()
    
    counter=1
    print "Let's send some bunnies..."
    while True:
    	try:
		tweet=""
                # Get a random bunny type and get a picture from Google
		rabbitType=random.choice(search_terms)
		url=get_random_image_url(rabbitType)
	        
		# Get random hashtags
		tag=""
		while(24+len(tweet)+len(tag)+len(BUNNY_HASHTAG)<=140):
			tweet+=tag
			tag=" "+random.choice(hashtags)		
    
		tweet=url+tweet+" "+BUNNY_HASHTAG
		
		# Send the bunny
		url = 'https://mobile.twitter.com/compose/tweet'
	        response = bot.get(url)
   
                html = fromstring(response.content)
                payload = dict(html.forms[0].fields)
                payload.update({'tweet[text]': tweet})
                bot.post("https://mobile.twitter.com/compose/tweet", data =payload)

		print "   \\\\"
		print "  __()"
		print "o(_-\_  "+str(counter)+" "+("bunny" if counter==1 else "bunnies")+" sent"
		time_to_sleep=random.randint(60*int(minTime),60*int(maxTime))
   		time.sleep(time_to_sleep)
		counter+=1

        except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence! Let the rabbits get some rest now.\n'
                break
        #except HttpResponseError, e:
         #       msg = '[HttpResponseError]:'+e
	#	print msg
         #       with open("log_Error.txt", "a") as log:
          #          log.write(msg+"\n")
        except Exception,e:
                msg = '[CatchAllError]:'+str(e)
		print e
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")


def get_random_image_url(topic):
	rand=random.randint(1,50)
	t=requests.get("http://ajax.googleapis.com/ajax/services/search/images?q="+topic+"&v=1.0&rsz=large&start="+str(rand)).content
	decoded=json.loads(t)
	return decoded['responseData']['results'][0]['unescapedUrl']
	
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence! Let the rabbits get some rest now.\n')
