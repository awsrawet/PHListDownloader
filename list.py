from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import urllib.request
import sys
import requests


def download(url, filename):
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
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')

sys.path.append("./")
l = []
with open('list.txt') as csvfile:
    spamreader = csv.reader(csvfile,delimiter="\n")
    for row in spamreader:
        l.append(row[0][:-1])
driver = webdriver.Firefox()
driver.set_page_load_timeout(30)
driver.implicitly_wait(20)
i=1
for x in l:
    driver.get("https://xxxsave.net")
    urlb = driver.find_element_by_name("url")
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
    print("Downloading video"+str(i)+".mp4")
    # resp = urllib.request.urlretrieve(video_url, 'video'+str(i)+'.mp4')
    download(video_url,'video'+str(i)+'.mp4')
    i=i+1
    print("Download complete")
