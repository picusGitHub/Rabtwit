#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Name: Rabtwit (v.0.1.0)
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
# - Selenium (http://selenium-python.readthedocs.org)
# - NodeJS (https://nodejs.org/en/)
# - PhantomJS (http://phantomjs.org/) for --silent mode, Firefox or Chrome otherwise
# - Simplejson (https://pypi.python.org/pypi/simplejson)
#  
# 
# Usage:  python rabtwit.py -u <Twitter username> [--silent] [--tmin=<min minutes between tweets> --tmax=<max minutes between tweets>]
# Example: the command "python rabtwit.py -u exampleuser --silent --tmin=7 --tmax=13" will tweet a rabbit every 7 to 13 minutes
#           
# Linux/Unix:
# - Linux Pip install instructions: http://pip.readthedocs.org/en/stable/installing/
# - Requests module instructions: http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests (pip install requests) (pip install request[security])
# - Selenium module instructions : http://selenium-python.readthedocs.org/installation.html (pip install selenium)
# - NodeJS instructions: https://nodejs.org/en/download/
# - PhantomJS instructions: https://www.npmjs.com/package/phantomjs (npm install -g phantomjs)
# 
# Windows:
# - Make sure pip is installed: http://pip.readthedocs.org/en/stable/installing/
# - Open up cmd and run c:\python27\scripts\easy_install.exe request
# - Get the zip : https://github.com/cobrateam/splinter/archive/master.zip unzip on your disk, 
# open a terminal (start menu -> type cmd -> launch cmd.exe) 
# go in the folder you unzip splinter (cd XXXX) launch 'python setup.py install'
# - You may also need to open up cmd and run the following command: c:\python27\scripts\easy_install.exe request
# if the requests module is not installed
# 
# Need Help or Find a Bug?
# - /join #OpParis-Dev - https://webchat.anonops.com/?channels=OpParis-Dev and contact picus or any other rabbit
# 

import sys
import random
import simplejson as json
try:
    from selenium import webdriver
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.keys import Keys
    
except:
    print "Please install Selenium."
    print "* Unix/Linux Use: sudo pip install selenium"
    print "* Windows: See script's comments"
    print "* More Info: http://selenium-python.readthedocs.org"
    sys.exit()
try:
    import requests
except:
    print "Please install the requests module."
    print "* Unix/Linux Use: pip install requests"
    print "* Windows in CMD: c:\python27\scripts\easy_install.exe request"
    print "* More Info: http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests"
    sys.exit()
    
import getopt, re, time
import getpass

VERSION = "v 0.1.0"
HASHTAGS_FILE="hashtags.txt"
SEARCHTERMS_FILE="searchterms.txt"
RABBIT="rabbit_art.txt"
BUNNY_HASHTAG="#rabtwit"
DEFAULT_MIN_TIME=5
DEFAULT_MAX_TIME=10

def main(argv):
    username = None
    boot_screen="*******************************************************\n"
    boot_screen+="*                   RabTwit "+VERSION+"                   *\n"                                   
    boot_screen+="*         Let's flood twitter with cute bunnies!      *\n"
    boot_screen+="*******************************************************"	
    usageString = boot_screen+"\nUsage: python rabtwit.py -u <Twitter username>  [--silent] [--tmin=<min minutes between tweets> --tmax=<max minutes between tweets>] [-s]\n       If not specified, <min time between tweets> is set to 5, <max time between tweets> is set to 10"
    try:
        opts, args = getopt.getopt(argv,"h:u:",["user=","tmin=","tmax=","silent"])
    except getopt.GetoptError:
        print usageString
        sys.exit(2)

    minTime=None
    maxTime=None
    silent_mode=False

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
	elif opt == "--silent":
	    silent_mode=True

    #A few checks
    if not username:
        print usageString
	print username+"*******************"
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


# comment this line if you want to use privoxy + tor:
    browser=None
    if(silent_mode):
	try:
    		browser=webdriver.PhantomJS()
	except:
		print "Please install PhantomJS."
		print "* npm install -g phantomjs"
		print "* More info: https://www.npmjs.com/package/phantomjs"
		sys.exit()
    else:
	try:
		browser=webdriver.Firefox()
	except:
		try:
			browser=webdriver.Chrome()
		except:
			print "Please put Firefox or Chrome driver executables in PATH."
			sys.exit()
			

    browser.set_window_size(1120, 550)
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
#    with Browser('firefox',profile_preferences=proxy_settings) as browser:
    try:
	print "Connecting to twitter..."
    	browser.get("https://mobile.twitter.com/session/new")
        time.sleep(1)
        browser.execute_script("document.getElementById('session[username_or_email]').value='"+username+"';")
        browser.execute_script("document.getElementById('session[password]').value='"+password+"';")
        browser.find_element_by_css_selector("input[type='submit']").click()
        time.sleep(1)

        if "https://mobile.twitter.com/login/error" in browser.current_url:
        	print "Twitter login Failed!"
                sys.exit()
	
	hashtags=open(HASHTAGS_FILE).read().splitlines()
	search_terms=open(SEARCHTERMS_FILE).read().splitlines()

    except Exception,e:
    	print "Unexpected error occured while trying the Twitter login. Please try running the script again."
	print e
        sys.exit()

    print "Twitter login done!"
    counter=1
    while True:
    	try:
		print "Let's send some bunnies..."
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
		browser.get("https://mobile.twitter.com/compose/tweet")
		browser.execute_script('document.getElementsByClassName("tweetbox")[0].value="'+tweet+'";')
		time.sleep(1)	
		browser.find_element_by_css_selector("input[type='submit']").click()

		print "   \\\\"
		print "  __()"
		print "o(_-\_  "+str(counter)+" "+("bunny" if counter==1 else "bunnies")+" sent"
		time_to_sleep=random.randint(60*int(minTime),60*int(maxTime))
   		time.sleep(time_to_sleep)
		counter+=1

        except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence! Let the rabbits get some rest now.\n'
                break
        except HttpResponseError, e:
                msg = 'HttpResponseError'
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")
        except Exception,e:
                msg = 'CatchAllError'
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
