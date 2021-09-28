from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import urllib.request
import sys
import requests
from selenium.webdriver.chrome.options import Options
import threading
import time

options = Options()
options.headless = True

obj = threading.Semaphore(10)#Calculate using your bandwith for optimal result n = Bandwith(mbps)x2 (since xxxsave.net limits downloads to 500kbps)



def download(url, filename):
    obj.acquire()
    print("Downloading video-"+filename+".mp4")

    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
    print("Download complete")
    obj.release()
    

l = []
with open('list.txt') as csvfile:
    spamreader = csv.reader(csvfile,delimiter="\n")
    for row in spamreader:
        l.append(row[0][:-1])
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)
driver.implicitly_wait(20)
for x in l:
    driver.get("https://xxxsave.net")
    urlb = driver.find_element_by_name("url")
    print(x)
    urlb.send_keys(x)
    sb = driver.find_element_by_id("bsubmit")
    sb.click()
    try:
        db = driver.find_element_by_xpath("//a[contains(@href,'1080P')]")
    except Exception:
        try:
            db = driver.find_element_by_xpath("//a[contains(@href,'720P')]")
        except Exception:
            try:
                db = driver.find_element_by_xpath("//a[contains(@href,'480P')]")
            except Exception:
                continue
    video_url = db.get_property('href')
    video_title = driver.find_element_by_xpath("//*[@class='vtitle']").text
    video_title = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    t = threading.Thread(target=download, args=(video_url,video_title+'.mp4'))
    t.start()
    

