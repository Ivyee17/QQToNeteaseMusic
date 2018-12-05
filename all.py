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
browser.get("https://y.qq.com/.....")  // input your url
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
    try:
        w=browser.find_element(By.ID,"page_box")
        w=w.find_element(By.TAG_NAME,'div')
        tt=w.find_element(By.CLASS_NAME,'next')
    except Exception as E:
        break
    ActionChains(browser).move_to_element(tt).perform()
    time.sleep(0.5)
    tt.click()
# print(musiclist)
m=numpy.array(musiclist)
numpy.save('musiclist.npy', m)

# Step 2: Find elements in netease music.
a=numpy.load('musiclist.npy')
musiclist=a.tolist()

for l in musiclist:
    # print()
    # print()

    # 处理字符串
    l=" ".join(l)
    # print(l)
    l = l.replace("%", "%25")
    l = l.replace("\n", "")
    if "" == l:
        continue
    # print(l)

    # URL搜索歌曲
    browser.get(
        "https://music.163.com/#/search/m/?s=" + l + "&type=1&type=1")
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[-1])
    t = None
    try:
        browser.switch_to.frame('contentFrame')
        t = browser.find_elements(By.CLASS_NAME, 'g-bd')[0]
        t = t.find_element_by_css_selector("[class='g-wrap n-srch']")
        t = t.find_element(By.ID, 'm-search')
        t = t.find_element_by_css_selector("[class='ztag j-flag']")
        t = t.find_element(By.CLASS_NAME, 'n-srchrst')
        t = t.find_element(By.CLASS_NAME, 'srchsongst')  # error if not found, but is it name problem??
        # print(l + " is found")
    except Exception as E:
        print(l + " not found")  # if here, no songs found.
        continue

    # 处理弹窗
    try:
        g2 = browser.find_element(By.CLASS_NAME, 'zcls')
        time.sleep(2)
        g2.click()
        # print("deal an extra window")
    except Exception as E:
        pass
        # print("Normal. Since if no pop up - zcls have, this will execute")

    # 歌曲录入
    try:
        tm = t.find_element_by_css_selector("[class='item f-cb h-flag  js-dis']")  # Precise detect
        print(l + ' this is grey')
    except Exception as E:
        try:
            t = t.find_elements(By.TAG_NAME, 'div')[0]  # same
            td = t.find_element_by_css_selector("[class='td w0']")
            td = td.find_element(By.CLASS_NAME, 'sn')
            td = td.find_element(By.CLASS_NAME, 'text')
            td = td.find_element(By.TAG_NAME, 'a')
            td = td.find_element(By.TAG_NAME, 'b')
            # print(td.get_attribute("title"))
            tf = t.find_elements(By.CLASS_NAME, 'td')
            tf = tf[2]
            tf = tf.find_element_by_css_selector("[class='opt hshow']")
            tfe = tf.find_element(By.TAG_NAME, 'a')
            time.sleep(2)
            ActionChains(browser).move_to_element(tfe).perform()
            tfe.click()
            # print("have clicked the black first line.")
        except Exception as E2:
            print(E2)
            print(l + " Not grey & can found but Exception happen!")
