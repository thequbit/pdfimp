pdfimp
======

Find PDFs from a URL


#####About#####


Web scraper that will go on to a URL and report back all 'application/pdf' typed links.
The number of link levels that are followed, start URL, base domain to look for, how much
of each link to download before it is typed, and a number of other URLs to search can be
passed into the scraping engine.


#####Usage#####


    >>> from pdfimp import pdfimp
    >>>
    >>> imp = pdfimp()
    >>> siteurl = "http://www.example.com/"
    >>> links = imp.getpdfs(maxlevel=2,siteurl=url,links=[url])
    >>> print links
    

