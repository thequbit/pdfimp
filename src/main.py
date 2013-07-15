#!/usr/bin/env python

from optparse import OptionParser

import magic
import urllib
import urllib2
from bs4 import BeautifulSoup
import hashlib

def getpagelinks(siteurl,url):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html)
    atags = soup.find_all('a', href=True)
    links = []
    for tag in atags:
        siteurlmatch = True
        if ( (len(tag['href']) >= 7 and tag['href'][0:7].lower() == "http://") or
             (len(tag['href']) >= 8 and tag['href'][0:8].lower() == "https://") or
             (len(tag['href']) >= 3 and tag['href'][0:3].lower() == "ftp://") ):
            if(url[:url.find("/",7)+1] != siteurl):
               siteurlmatch = False
            links.append((siteurlmatch,tag['href']))
        else:
            links.append((siteurlmatch,siteurl + tag['href']))
    return links

def typelink(link,filesize):
    req = urllib2.Request(link, headers={'Range':"byte=0-{0}".format(filesize)})
    success = True
    filetype = ""
    try:
        payload = urllib2.urlopen(req,timeout=5).read(filesize)
        filetype = magic.from_buffer(payload,mime=True)
    except:
        success = False;
    return success,filetype

def getpdfhash(link):
    success = True
    pdfhash = ""
    try:
        payload = urllib2.urlopen(link).read()
        pdfhash = hashlib.sha256(payload).hexdigest()
    except:
        success = False
    return success,pdfhash

def parseargs():
    parser = OptionParser(usage="usage: %prog [options] url",
                          version="%prog 1.0")

    parser.add_option("-s", "--silent",
                      action="store",
                      dest="silent",
                      default=False,
                      help="Do not print out any messages while running.")
    parser.add_option("-u","--siteurl",
                      action="store",
                      dest="siteurl",
                      default="",
                      help="Force the site url (ex: http://google.com/)")
    parser.add_option("-l","--levels",
                      action="store",
                      dest="levels",
                      default=1,
                      help="The number of link levels to scrape from the URL.")
    parser.add_option("-f","--filesize",
                      action="store",
                      dest="filesize",
                      default=1024,
                      help="The number of bytes to download before typing each link.")
    parser.add_option("-i","--ignore",
                      action="store_true",
                      dest="ignore",
                      default=True,
                      help="Ignore non-base-url links.")
    parser.add_option("-o","--output",
                      action="store",
                      dest="output",
                      default="output.txt",
                      help="Output file name. (default: output.txt)")

    (options,args) = parser.parse_args()

    if( len(args) < 1 ):
        parser.error("Wrong number of arguments, use -h for help.")

    return (options,args)

def tabs(level):
    rettext = ""
    for i in range(0,level):
        rettext = "{0}\t".format(rettext)
    return rettext

def getpdfs(ignore,filesize,maxlevel,level,ignorelinks,siteurl,link):
    pdfs = []
    if( level >= maxlevel ):
        return pdfs;
    
    level += 1
    print "{0}working on '{2}'".format(tabs(level),level,link)
    links = getpagelinks(siteurl,link)
    for _link in links:
        match,link = _link
        if( not (ignore == True and match == False) ):
#           if( not (link in ignorelinks) ):
                print "{0}{1}".format(tabs(level),link)
                typesuccess,filetype = typelink(link,filesize)
                if( typesuccess == True and (filetype.lower() == 'text/html') ):
                   _pdfs = [] 
                   _pdfs = getpdfs(ignore,filesize,maxlevel,level,ignorelinks,siteurl,link)
                   ignorelinks.append(link)
                   for pdf in _pdfs:
                       pdfs.append(pdf)
                if( typesuccess == True and (filetype.lower() == 'application/pdf') ):
                    hashsuccess,pdfhash = getpdfhash(link)
                    if( hashsuccess == True ):
                        print "{0}[INFO ] PDF Found".format(tabs(level))
                        pdfdoc = (pdfhash,link)
                        pdfs.append(pdfdoc)
    level -= 1
    return pdfs

def main():
    (options,args) = parseargs()

    url = args[0]
    if( options.siteurl == "" ):
        siteurl = url[:url.find("/",7)+1]
    else:
        siteurl = options.siteurl
    filesize = options.filesize
    ignore = options.ignore
    maxlevel = (int)(options.levels)
    level = (int)(0)
    ignorelinks = []

    print "Running with level = {0}, Max = {1}".format(level,maxlevel)

    pdfs = getpdfs(ignore,filesize,maxlevel,level,ignorelinks,siteurl,url)

    print pdfs

if __name__ == '__main__':
    main()
