from argparse import Action
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import numpy
from selenium.webdriver.common.keys import Keys

# Step 0-1: Define some variables:
musiclist = []

# Step 0-2: Init environment.
chromeOptions = webdriver.ChromeOptions()
chromeOptions._arguments = ['disable-infobars']
# chromeOptions.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chromeOptions)
# browser = webdriver.Chrome(chrome_options=chrome_options)  # code useful if want to set Chrome invisible

# Step 1: Find my elements in tencent music.
# below my music list - need change each time load a new list to netease
browser.get("https://y.qq.com/....")  # input your url here!
while 1:
    time.sleep(2) # wait until web is loaded. adjust by machine-depenedent
    mylist = browser.find_elements(By.CLASS_NAME, 'songlist__list')[0]
    mylist = mylist.find_elements(By.TAG_NAME, 'li')
    for e in mylist:
        e = e.find_element(By.CLASS_NAME, 'songlist__item')
        e1 = e.find_element(By.CLASS_NAME, "songlist__songname")
        e1 = e.find_element(By.CLASS_NAME, 'songlist__songname_txt')
        e1 = e1.find_element(By.TAG_NAME, 'a')
        string1 = e1.get_attribute("title")
        # print(e1.get_attribute("title"))
        e2 = e.find_element(By.CLASS_NAME, 'songlist__artist')
        e2 = e2.find_element(By.TAG_NAME, 'a')
        string2 = e2.get_attribute("title")
        # print(e2.get_attribute("title"))
        e3 = e.find_element(By.CLASS_NAME, 'songlist__album')
        e3 = e3.find_element(By.TAG_NAME, 'a')
        string3 = e3.get_attribute("title")
        # print(e3.get_attribute("title")+" find.")
        musiclist.append([string1, string2, string3])
    w=browser.find_element(By.ID,"page_box")
    w=w.find_element(By.TAG_NAME,'div')
    try:
        tt=w.find_element(By.CLASS_NAME,'next')
    except Exception as E:
        break
    ActionChains(browser).move_to_element(tt).perform()
    time.sleep(0.5)
    tt.click()
print(musiclist)
m=numpy.array(musiclist)
numpy.save('musiclist.npy', m)
