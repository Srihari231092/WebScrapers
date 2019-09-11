import os
from urllib.request import urlopen as uReq, urlretrieve
from bs4 import BeautifulSoup as soup
import time
import re, string

# NewEgg example
def new_egg_example():
    print(os.getcwd())
    my_url = "https://www.newegg.com/p/pl?Submit=ENE&IsNodeId=1&N=100021392%20600489407%20600489408%20600538759%20600560190&name=Steam-PC-Download"

    # Opening a connection, grabbing the page
    client = uReq(my_url)

    # Save the download into an object
    page_html = client.read()

    # Close the client
    client.close()

    # Clean up the HTML code
    page_soup = soup(page_html, "html.parser")

    # Get the objects of interest. Here they're div elements with a class of "item-container"
    containers = page_soup.findAll(name="div", attrs={"class":"item-container"})

    ctr = 0

    for container in containers:
        imgs = container.findAll(name="img")
        for img in imgs:
            img_src = str(img.attrs['src'])
            if "/Brandimage" in img_src:
                continue
            print(img_src)
            item_title = container.findAll(name="a", attrs={"class": "item-title"})[0]
            print(item_title.text)
            fname = item_title.text
            fname = re.sub('[\W_]+', '', fname)
            urlretrieve("https:"+img_src, fname+".jpg")
            ctr +=1
            time.sleep(0.5)


my_url = "https://steamcommunity.com/app/1097840/reviews/?browsefilter=toprated&snr=1_5_100010_"

# Opening a connection, grabbing the page
client = uReq(my_url)

# Save the download into an object
page_html = client.read()

# Close the client
client.close()

# Clean up the HTML code
page_soup = soup(page_html, "html.parser")

# Get the reviews
review_elems = page_soup.findAll(name="div", attrs={"class":"apphub_CardTextContent"})

for review_elem in review_elems:
    date_posted = review_elem.findAll(name="div", attrs={"class":"date_posted"})[0].text
    unclean_review = review_elem.text
    review = ""
    for ucr in unclean_review.split("\t"):
        if (date_posted in ucr) or (len(ucr)==0):
            continue
        review += ucr
        review += "\n"
    # Sanity check - remove trailing white space
    review = review.strip()
    print(date_posted, "\n\t", review)
    print(80*"-")