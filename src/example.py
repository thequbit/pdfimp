import time

from pdfimp import pdfimp

def main():
    
    start_time = time.time()

    siteurl = "http://www.scottsvilleny.org/"
    imp = pdfimp()
    links = imp.getpdfs(maxlevel=maxlevel,siteurl=siteurl,links=[siteurl])

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

