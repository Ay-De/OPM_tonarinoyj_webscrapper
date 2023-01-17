from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import xml.etree.ElementTree as ET
import re

from modules.webdriver import setup_webdriver

class HeadlessBrowser:
    
    def __enter__(self):
        
        class Downloader:
            def __init__(self):

                self.chapters = {}

                self.options = Options()
                self.options.add_argument('headless')
                self.options.add_argument('window-size=1920x1080')
                self.options.add_argument('disable-extensions')
                self.webdriver = webdriver.Edge(options=self.options)

                self.OPM_chapters_url = 'https://tonarinoyj.jp/atom/series/13932016480028984490'
                self._get_chapters(self.OPM_chapters_url)


            def _get_chapters(self, chapters_url):
                self.webdriver.get(chapters_url)

                xx = self.webdriver.find_element(by=By.TAG_NAME, value='body').text
                namespaces = {'xmlns': "http://www.w3.org/2005/Atom"}
                self.tree = ET.fromstring(xx)
                for e in self.tree.findall('{http://www.w3.org/2005/Atom}entry'):
                    title = e.find('{http://www.w3.org/2005/Atom}title').text
                    title = re.findall(r"[0-9]+", title)
                    url = e.find('{http://www.w3.org/2005/Atom}link').get('href')

                    if title:
                        self.chapters.update({title[0]: url})
                        
                
                #print('link:{} {}'.format(self.link, self.link.get('href')))


        self.headless_browser = Downloader()
        return self.headless_browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.headless_browser.webdriver.quit()


def main():

    setup_webdriver()

    with HeadlessBrowser() as headless:

        print(headless.chapters['1'])

        print("ok")


if __name__ == '__main__':
    main()