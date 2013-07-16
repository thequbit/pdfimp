import time

from pdfimp import pdfimp

def main():

    level = 0
    maxlevel = 1
    filesize = 1024

    siteurl = "http://www.scottsvilleny.org/"
    #success,linktype = typelink(siteurl,filesize)
    urls = []
    urls.append(siteurl)

    start_time = time.time()

    imp = pdfimp()

    links = imp.getlinks(level,maxlevel,filesize,siteurl,urls,True)

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

