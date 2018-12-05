from argparse import Action
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

# Step 0-1: Define some variables:
musiclist = []

# Step 0-2: Init environment.
chromeOptions = webdriver.ChromeOptions()
chromeOptions._arguments = ['disable-infobars']
browser = webdriver.Chrome(chrome_options=chromeOptions)
# browser = webdriver.Chrome(chrome_options=chrome_options)  # code useful if want to set Chrome invisible


# Step 2: Find elements in netease music.
f = open('log.txt', 'r', encoding='utf-16')
while 1:
    line = f.readline()
    musiclist.append(line)
    if not line:
        break

for l in musiclist:
    # print()
    # print()

    # 处理字符串
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



# After:
# Make new tab, login, save this list. (netease music protect from selenium.)

# 注意%应改为%25
