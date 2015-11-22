#!/usr/bin/env python
#-*- coding: utf-8 -*-
#python twitterReport.py -u <Twitter username> -i <account_list.txt>
import sys, getopt, re, os

try:
    from splinter import Browser
except:
    print "Please install Splinter: http://splinter.readthedocs.org/en/latest/install.html"
    sys.exit()

import sys, getopt, re, os
from datetime import datetime
import splinter
from splinter.request_handler.status_code import HttpResponseError
import getpass
from selenium import webdriver

f = webdriver.Firefox()

def main(argv):
    d = datetime.now()
    date = str(d.year) + '' + str(d.month) + '' + str(d.day) + '' + str(d.hour) + '' + str(d.minute) + '' + str(d.second)
    username = "wildhacks"
    txt = None
    try:
        opts, args = getopt.getopt(argv,"hi:u:",["file=","user=","help"])
    except getopt.GetoptError:
        print 'Use --help for help'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'Usage: %s <options> \n' % (os.path.basename(__file__))
            print '     -h, --help              This help'
            print '     -u, --user USERNAME     Your Twitter username'
            print '     -f, --file FILE         File with twitter URLs list'
            sys.exit()
        elif opt in ("-i", "--file"):
            txt = arg
        elif opt in ("-u", "--user"):
            username = arg

    if not username and not txt:
        print 'Use --help for help\n'
        print 'Usage: python twitterReport.py -u <Twitter username> -i <account_list.txt>'
        print 'The accounts list must have only 1 account per line'
        sys.exit()

    password = getpass.getpass()

# comment this line if you want to use privoxy + tor:
    with Browser() as browser:
#uncomment this section if you want to use privoxy + tor:
    # proxyIP = '127.0.0.1'
    # proxyPort = 8118

    # proxy_settings = {'network.proxy.type': 1,
    #         'network.proxy.http': proxyIP,
    #        'network.proxy.http_port': proxyPort,
    #        'network.proxy.ssl': proxyIP,
    #        'network.proxy.ssl_port':proxyPort,
    #        'network.proxy.socks': proxyIP,
    #        'network.proxy.socks_port':proxyPort,
    #        'network.proxy.ftp': proxyIP,
    #        'network.proxy.ftp_port':proxyPort
    #        }

    #with webdriver.Firefox() as browser:
        browser.visit("http://twitter.com/")
        #wait for browser to load

        #print username 
        browser.execute_script("$('#front-container #signin-email').val('%s');"  % (username))
        browser.execute_script("$('#front-container #signin-password').val('%s');" % (password))
        browser.find_by_css("button[type='submit'].submit.btn.primary-btn").click()

        if "https://twitter.com/login/error" in browser.url:
            print "The email and password you entered did not match our records."
            sys.exit()

        try:
            file = open(txt, 'r')
        except:
            print "Unable to open file"
            sys.exit()

        for line in file:
            try:
                url = re.match(r"(?:https:\/\/)?(?:http:\/\/)?(?:www\.)?twitter\.com/(#!/)?@?([^/\s]*)",line.strip())
                url = url.group()
                browser.visit(url)
                if not browser.is_element_present_by_css('.route-account_suspended'):
                    browser.find_by_css('.user-dropdown').click()
                    browser.find_by_css('li.report-text button[type="button"]').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='abuse']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='harassment']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='Someone_else']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='violence']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()
                    followers = browser.find_by_css('a[data-nav="followers"] .ProfileNav-value').value;
                    msg = url.strip()+' - ' + followers + ' Followers'
                    with open("log_reported_"+date+".txt", "a") as log:
                        log.write(msg+"\n")
                elif browser.is_element_present_by_css('.route-account_suspended'):
                    msg =  line.strip()+' - Suspended'
                    with open("log_suspended.txt", "a") as log:
                        log.write(msg+"\n")
                else:
                    msg = line.strip()+' - Unknown'
                    with open("log_unknown.txt", "a") as log:
                        log.write(msg+"\n")

                print msg

            except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence!'
                break
            except HttpResponseError:
                msg = line.strip()+' - HttpResponseError'
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")
            except:
                if line:
                    msg = url.strip()+' - CatchAllError'
                    print msg
                    with open("log_Error.txt", "a") as log:
                        log.write(msg+"\n")
                else:
                    pass

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence!')
