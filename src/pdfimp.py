
import time
import magic
import urllib
import urllib2
from bs4 import BeautifulSoup
import hashlib

class pdfimp:

    _verbose = False

    def __init__(self):
        self._verbose = True

    def _report(self,text):
        if self._verbose == True:
            print text
    
    def _getpagelinks(self,siteurl,url):
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
    
    def _typelink(self,link,filesize):
        req = urllib2.Request(link, headers={'Range':"byte=0-{0}".format(filesize)})
        success = True
        filetype = ""
        try:
            payload = urllib2.urlopen(req,timeout=5).read(filesize)
            filetype = magic.from_buffer(payload,mime=True)
        except:
            success = False;
        return success,filetype
    
    def getlinks(self,level,maxlevel,filesize,siteurl,links,verbose):
        retlinks = []
        if( level >= maxlevel ):
            self._report("[INFO   ] Max depth reached.")
        else:
            level += 1
            for link in links:
    
                ignored = 0            
    
                self._report("[INFO   ] Getting links for '{0}'".format(link))
                pagelinks = self._getpagelinks(siteurl,link)
                self._report("[INFO   ] Found {0} links ...".format(len(pagelinks)))
                
                thelinks = []
                for _pagelink in pagelinks:
                    match,pagelink = _pagelink
                    if( match == True ): #and ( (level != maxlevel) or (level == maxlevel and (not pagelink in retlinks) ) ) ):
                        thelinks.append(pagelink)
                
                gotlinks = self.getlinks(level,maxlevel,filesize,siteurl,thelinks,verbose)
                for gotlink in gotlinks:
                    if not any(gotlink in r for r in retlinks):
                        success,linktype = self._typelink(gotlink,filesize)
                        if success == True and linktype == 'application/pdf':
                            retlinks.append((linktype,gotlink))
                            self._report("[INFO   ] Added '{0}'".format(gotlink))
                        else:
                            ignored += 1
    
                for thelink in thelinks:
                    if not any(thelink in r for r in retlinks):
                        success,linktype = self._typelink(thelink,filesize)
                        if success == True and linktype == 'application/pdf':
                            retlinks.append((linktype,thelink))
                            self._report("[INFO   ] Added '{0}'".format(thelink))
                        else:
                            ignored += 1
    
                self._report("Ignored Links: {0}/{1}".format(ignored,len(pagelinks)))
    
            level -= 1
        return retlinks

