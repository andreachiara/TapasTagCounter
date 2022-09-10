from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re

filename = "sel_result2.tsv"
queer_num = 0
tot_num = 0
acc_tags = re.compile("queer|bl|gl|yaoi|yuri|boys love|boyslove|boys_love|girls_love|girls love|girlslove|shounenai|shounen ai|shonen ai|shonenai|shonen_ai|shounen_ai|shōnen_ai|shōnen ai|shoujo_ai|shoujo ai|shojo ai|shojoai|shoujoai|shōjoai|shōjo ai|shōjo_ai|girls love|lgbt|lgbtq|lgbtq+|lgbtqai|lgbtqai+|lgbtqia|lgbtqia+|lgbtqa|lgbtqa+|intersexual|intersequality|intersex|asexual|asexuality|pansexual|pansexuality|aromantic|lesbian|gay|bisexual|bisexuality|trans|transgender|nonbinary|enby|ftm|mtf|genderfluid|genderqueer|crossdress|crossdressing|transmasc|transfemme|transfeminine|transmasculine|sexual orientation|gender identity|homosexuality|hrt|soft_bl|soft_gl|wlw|mlm|nblm|nblw|nblnb|wlnb|mlnb")
title_re = re.compile("(?<=Read ).*?(?=\| Tapas Web Comics)")


links = []

with open(filename, 'a') as f:
    f.write('title\tqueer?\tyes/all\t%\ttags\turl\n')


class Sel(unittest.TestCase):
    def setUp(self):
        from selenium import webdriver 
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        chrome_options.headless = True # also works
        self.driver = webdriver.Chrome(options=chrome_options)
        #self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(0)
        self.base_url = "https://tapas.io"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        global filename
        global links
        global queer_num
        global tot_num
        global acc_tags
        global title_re

        driver = self.driver
        delay = 1
        driver.get(self.base_url + "/comics?b=ALL&g=0&f=NONE&s=DATE")
        #driver.find_element(By.LINK_TEXT, 'All').click()
        for i in range(1,4718):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print ("scroll: " + str(i))
            time.sleep(1)
        #html_source = driver.page_source
        #data = html_source.encode('utf-8')
        els = driver.find_elements(By.CLASS_NAME, 'thumb')

        for el in els:
            links.append(el.get_attribute('href'))
        print("found " + str(len(links)) + " links: " + str(links))

        for link in links:
            driver.get(link + "/info")
            tags = driver.find_elements(By.CLASS_NAME, 'tags__item')
            genres = driver.find_elements(By.CLASS_NAME, 'genre-btn')
            title_raw = driver.find_element(By.TAG_NAME, "title").get_attribute("innerHTML")
            title_allmatch = title_re.search(title_raw)
            if (title_allmatch is None):
                continue

            tot_num += 1
            title = title_allmatch.group(0)
            alltags = ""
            for tag in tags:
                #if (tag.text != ""):
                alltags += str(tag.get_attribute("innerHTML")) + ","
            for genre in genres:
                #if (genre.text != ""):
                alltags += str(genre.text) + ","
            is_queer = False
            queer_str = "No"
            tags_lower = str(alltags).lower()
            if (acc_tags.search(tags_lower)):
                is_queer = True
                queer_str = "YESSSSS"
                queer_num += 1
            with open(filename, 'a') as f:
                f.write(str(title) + '\t' + queer_str + '\t' + str(queer_num) + '/' + str (tot_num) + '\t' + str((queer_num/tot_num)*100) + '\t"' + tags_lower + '"\t"' + str(link) + '"\n')
            print('Saved file %s' % filename)
            print (link + " : " + str(alltags))



if __name__ == "__main__":
    unittest.main()