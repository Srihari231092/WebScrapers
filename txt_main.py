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
