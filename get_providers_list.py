from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(executable_path='./chrome_driver/chromedriver.exe', options=chrome_options)

link = 'https://alternativedata.org/data-providers/'
driver.get(link)
raw_html = driver.page_source

time.sleep(5)
close_modal = True
page = 1
load_more_btn = driver.find_element_by_css_selector('a.load-more')
while load_more_btn.value_of_css_property('display') != 'none':
    try:
        driver.find_element_by_css_selector('a.load-more').click()
    except BaseException as err:
        print(str(err))
    if close_modal:
        try:
            driver.find_element_by_css_selector('button.close').click()
            close_modal = False
        except BaseException as err:
            print(str(err))
    time.sleep(3)
    page += 1
    print(page)

raw_html = driver.page_source
driver.quit()

with open(f'./altdataorg_html/altdataorg_20210128.html', 'w', encoding='utf-8') as f:
    f.write(raw_html)

