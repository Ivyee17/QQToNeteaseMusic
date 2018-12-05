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


# Step 2: Find elements in netease music.
aa=numpy.load('musiclist.npy')
musiclist=aa.tolist()
for l in musiclist:
    browser.get(
        "https://music.163.com/#/search/m/?s=" + l[0] + " " + l[1] + " " + l[2] + "&type=1&type=1")
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
        # print(t.get_attribute("title"))
    except Exception as E:
        print(l)  ### if here, no songs found.
        continue
    try:
        if t != None:
            t = t.find_elements(By.TAG_NAME, 'div')[0]
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
            ActionChains(browser).move_to_element(tfe).perform()
            time.sleep(2)
            tfe.click()
    except Exception as E:
        print(" ".join(l) + " Exception happen!")

# After:
# Make new tab, login, save this list. (netease music protect from selenium.)