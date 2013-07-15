
import time
import magic
import urllib
import urllib2
from bs4 import BeautifulSoup
import hashlib

def getpagelinks(siteurl,url):
    links = []
    try:
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html)
        atags = soup.find_all('a', href=True)
        for tag in atags:
            siteurlmatch = True
            if ( (len(tag['href']) >= 7 and tag['href'][0:7].lower() == "http://") or
                 (len(tag['href']) >= 8 and tag['href'][0:8].lower() == "https://") or
                 (len(tag['href']) >= 3 and tag['href'][0:6].lower() == "ftp://") ):
                if(url[:url.find("/",7)+1] != siteurl):
                    siteurlmatch = False
                links.append((siteurlmatch,tag['href']))
            else:
                links.append((siteurlmatch,siteurl + tag['href']))
    except:
        links = []
    return links

def typelink(,filesize):
    req = urllib2.Request(link, headers={'Range':"byte=0-{0}".format(filesize)})
    success = True
    filetype = ""
    try:
        payload = urllib2.urlopen(req,timeout=5).read(filesize)
        filetype = magic.from_buffer(payload,mime=True)
    except:
        success = False;
    return success,filetype

def getlinks(level,maxlevel,filesize,siteurl,links):
    retlinks = []
    if( level >= maxlevel ):
        print "[INFO   ] Max depth reached."
    else:
        level += 1
        for link in links:
            print "[INFO   ] Getting links for '{0}'".format(link)
            pagelinks = getpagelinks(siteurl,link)
            print "[INFO   ] Found {0} links ...".format(len(pagelinks))
            thelinks = []
            for _pagelink in pagelinks:
                match,pagelink = _pagelink
                if( match == True and ( (level != maxlevel) or (level == maxlevel and (not pagelink in retlinks) ) ) ):
                    thelinks.append(pagelink)
            gotlinks = getlinks(level,maxlevel,siteurl,thelinks)
            for gotlink in gotlinks:
                if not gotlink in retlinks:
                    retlinks.append((linktype,gotlink))
                    print "[INFO   ] Added '{0}'".format(gotlink)
            for thelink in thelinks:
                if not thelink in retlinks:
                    linktype = typelink(thelink,filesize)
                    retlinks.append((linktype,thelink))
                    print "[INFO   ] Added '{0}'".format(thelink)
        level -= 1
    return retlinks

def main():

    siteurl = "http://www.scottsvilleny.org/"
    urls = []
    urls.append(siteurl)

    level = 0
    maxlevel = 10

    start_time = time.time()

    links = getlinks(level,maxlevel,siteurl,urls)

    end_time = time.time()

    print "" 
    print "---- STATS ----"
    print ""
    print "Site: {0}".format(siteurl)
    print "Link Levels: {0}".format(maxlevel)
    print "Total Links: {0}".format(len(links))
    print "Total Time: {0}".format(end_time-start_time)
    print ""

main()
