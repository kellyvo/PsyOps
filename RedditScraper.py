import praw
import sys

def writeURLsTo(filename, url, filemode):
    with open(filename, filemode) as f:
        f.write(url+"\n")

def getWebsite(website):
    if("https://" in website):
        website=website[8:]
    elif("http://" in website):
        website=website[7:]

    extension=website.find('/')
    website=website[0:extension]
    if("www." in website):
        website=website[4:]
    if(".com" in website or ".org" in website or ".gov" in website):
        website=website[:-4]
    return website

def addToDict(link, links):
    website=getWebsite(link)
    if(website not in links):
        links[website]=list()
    links[website].append(link)

def scrapeURLs():
    #Opens a praw instance in reddit
    reddit_instance=praw.Reddit(
        client_id='ZfutrHRAC9iUAg',
        client_secret='XE3kaUoCf5RWE0pRnsIhlH3aZss',
        user_agent='my_user_agent'
    )

    links=dict()
    allLinks=list()

    #time_filter="day"

    for link in reddit_instance.subreddit(sys.argv[1]).hot(limit=1000):
        if("reddit" not in link.url):
            allLinks.append(link.url)
            addToDict(link.url, links)

    for website in links.keys():
        for link in links[website]:
            writeURLsTo("./links/"+website+".txt", link, 'a')

    for link in range(len(allLinks)):
        writeURLsTo("./input.txt", allLinks[link], 'a')
        #if(link==0):
        #    writeURLsTo("./input.txt", allLinks[link], 'w')
        #else:
        #    writeURLsTo("./input.txt", allLinks[link], 'a')

if __name__=='__main__':
    scrapeURLs()