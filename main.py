import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import xml.etree.ElementTree as ET
import re

from modules.webdriver import setup_webdriver


class HeadlessBrowser:

    def __enter__(self):

        class TonariScrapper:

            manga_url = \
                'https://tonarinoyj.jp/atom/series/13932016480028984490'

            def __init__(self):

                self.chapters = {}

                self.options = Options()
                self.options.add_argument('headless')
                self.options.add_argument('window-size=1920x1080')
                self.options.add_argument('disable-extensions')
                self.webdriver = webdriver.Edge(options=self.options)

                self._get_chapters_links(TonariScrapper.manga_url)

            def _get_chapters_links(self, url):

                self.webdriver.get(url)

                self.tree = self.webdriver.find_element(by=By.TAG_NAME,
                                                        value='body').text

                self.tree = ET.fromstring(self.tree)

                for e in self.tree.findall(
                        '{http://www.w3.org/2005/Atom}entry'):
                    title = e.find('{http://www.w3.org/2005/Atom}title').text
                    title = re.findall(r"[0-9]+", title)
                    url = e.find('{http://www.w3.org/2005/Atom}link').get('href')

                    if title:
                        if int(title[0]) > 220:
                            self.chapters.update({title[0]: url})

                            self._get_image_links(title[0], url)

                # print('link:{} {}'.format(self.link, self.link.get('href')))

            def _get_image_links(self, chapter_num, chapter_url):

                self.webdriver.get('view-source:' + chapter_url + '.json')
                self.content = self.webdriver.page_source
                self.chapter_content = self.webdriver.find_element(By.CLASS_NAME,
                                                         'line-content').text
                self.chapter_data = json.loads(self.chapter_content)
                self.chapter_pages = \
                            self.chapter_data['readableProduct']['pageStructure']['pages']

                self._page_num = 0
                self._chapter = { }
                for page in self.chapter_pages:
                    if 'src' in page:
                        self._page_num = self._page_num + 1
                        self._page_link = page['src']

                        self._chapter.update({str(self._page_num): self._page_link})

                self.chapters.update({chapter_num: self._chapter})

        self.headless_browser = TonariScrapper()
        return self.headless_browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.headless_browser.webdriver.quit()


def main():
    setup_webdriver()

    with HeadlessBrowser() as headless:
        print(headless.chapters['221'])

        print("ok")


if __name__ == '__main__':
    main()
