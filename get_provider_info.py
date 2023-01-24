from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from random import randint
import json
import time
import os

with open('./altdataorg_html/altdataorg_20210128.html','r',encoding='utf8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

links = [e['href'] for e in soup.select('table a.orange')]
processed_links = [f.replace('.json','') for f in os.listdir('./provider_info/data/')]


for link in links:
    comp_id = link.split('/')[-2]
    if comp_id in processed_links:
        continue

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path='./chrome_driver/chromedriver.exe', options=chrome_options)

    output = {'id': comp_id, 'link':link}

    driver.get(link)
    output['name'] = driver.find_element_by_css_selector('.description>h1').text

    logo = driver.find_elements_by_css_selector('.logo>img')
    if len(logo) > 0:
        output['logo_url'] = logo[0].get_attribute('src')
        with open(f'./provider_info/logos/{comp_id}.png', 'wb') as f:
            f.write(logo[0].screenshot_as_png)
    else:
        output['logo_url'] = ''

    output['desc'] = driver.find_element_by_css_selector('.description>.big').text

    infoboxes_white = driver.find_elements_by_css_selector('.infobox.white')
    for ib in infoboxes_white:
        out = ib.text.split('\n')
        if len(out) == 2:
            output[out[1].lower().replace(' ', '_')] = out[0]

    infoboxes = driver.find_elements_by_css_selector('.numbers>.infobox')
    for ib in infoboxes:
        out = ib.text.split('\n')
        if len(out) == 2:
            if len(ib.find_elements_by_css_selector('p>a')) > 0:
                out[1] = ib.find_element_by_css_selector('p>a').get_attribute('href')
            output[out[0].lower().replace(' ','_')] = out[1]

    with open(f'./provider_info/data/{comp_id}.json', 'w') as f:
        json.dump(output,f,indent=2)


    time.sleep(randint(5, 25))
    driver.quit()