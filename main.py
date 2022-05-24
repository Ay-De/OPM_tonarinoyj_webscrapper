import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import xml.etree.ElementTree as ET
from lxml import etree

from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt
import time
from pyparsing import makeHTMLTags


class HeadlessBrowser:
    def __enter__(self):

        class Downloader:
            def __init__(self):
                self.options = Options()
                # options.add_argument('headless')
                self.options.add_argument('window-size=1920x1080')
                self.options.add_argument('disable-extensions')
                self.webdriver = webdriver.Edge(options=self.options)

                self.OPM_chapters_url = 'https://tonarinoyj.jp/atom/series/13932016480028984490'
                self._get_chapters(self.OPM_chapters_url)

            def _get_chapters(self, chapters_url):
                self.webdriver.get(chapters_url)
                #x = requests.get(chapters_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50'})
                #self.xmldoc = etree.fromstring(x.text)

                #self.parser = etree.XMLParser(recover=True)
                xx = self.webdriver.find_element(by=By.TAG_NAME, value='body').text
                namespaces = {'xmlns': "http://www.w3.org/2005/Atom"}
                self.tree = ET.fromstring(xx)

                for e in self.tree.findall('{http://www.w3.org/2005/Atom}entry'):
                    name = e.find('{http://www.w3.org/2005/Atom}title')
                    l = e.find('{http://www.w3.org/2005/Atom}link')
                    print(name.text, l.get('href'))

                res = [t.text for t in self.elems]
                print(self.elems)
             #   for child in self.tree:
             #       for l in child:
             #           print(child.tag, child.text)

            #    self.tree.iter('{http://www.w3.org/2005/Atom}link href')

            #    for t in self.tree.findall('title', namespaces=namespaces):
            #        print(t.tag, t.attrib)


               # print('link: {}'.format(self.link))
                print('link:{} {}'.format(self.link, self.link.get('href')))


        self.headless_browser = Downloader()
        return self.headless_browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.headless_browser.webdriver.quit()


def main():

    with HeadlessBrowser() as headless:
        print("ok")

    # url = 'https://tonarinoyj.jp/episode/13932016480028985383'
    # xhr_url = 'https://tonarinoyj.jp/atom/series/13932016480028984490'
    #
    # options = Options()
    # #options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # #options.add_argument('window-size=3840x2160')
    #
    #
    # driver = webdriver.Edge(options=options)
    #
    # driver.get(url)
    # next2 = driver.find_element(by=By.XPATH, value="//span[@class='viewer-btn-expand js-viewer-btn-expand']")
    # next2.click()
    #
    # try:
    #     while True:
    #         next = driver.find_element(by=By.XPATH, value="//a[@class='page-navigation-forward rtl js-slide-forward']")
    #         next.click()
    #         time.sleep(0.5)
    #         #print(next.get_attribute('class'))
    # except:
    #     print('end of comic')
    #
    # next.click()
    # time.sleep(0.5)
    # next.click()
    #
    # time.sleep(1)
    # driver.get_screenshot_as_file('test.png')
    # img = driver.get_screenshot_as_png()
    # img = np.asarray(Image.open(io.BytesIO(img)))
    #
    # print(img.shape)
    # with Image.open('test.png') as i:
    #     print(np.asarray(i).shape)
    #
    # plt.imshow(img)
    # plt.imshow(i)
    # plt.show()
    # driver.quit()
    #
    # print("asd")
    # with requests.Session() as sess:
    #     sess.get(url, headers=headers)
    #     response = sess.get(xhr_url, headers=headers, params={'free_only': '1'})
    #     print(response.content)

if __name__ == '__main__':
    main()