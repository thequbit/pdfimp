import time
from pprint import pprint
from pdfimp import pdfimp

def main():
    
    start_time = time.time()

    siteurl = "http://www.scottsvilleny.org/"
    maxlevel = 1
    imp = pdfimp()
    links = imp.getpdfs(maxlevel=maxlevel,siteurl=siteurl,links=[(siteurl,"")])

    end_time = time.time()

    pprint(links)

    print ""
    print "---- STATS ----"
    print ""
    print "Site: {0}".format(siteurl)
    print "Link Levels: {0}".format(maxlevel)
    print "Total Links: {0}".format(len(links))
    print "Total Time: {0}".format(end_time-start_time)
    print ""

main()

