import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
import xml.etree.ElementTree as ET
import re

from modules.webdriver import setup_webdriver
from modules.helpers import download


class HeadlessBrowser:

    def __enter__(self):

        class TonariScrapper:

            def __init__(self):

                self.manga_url = \
                    'https://tonarinoyj.jp/episode/316190247133138894'
                # 'https://tonarinoyj.jp/atom/series/13932016480028984490'
                self.download_location = 'D:\OPM\\'

                self.chapter_links = {}

                self.options = Options()
                # self.options.add_argument('headless')
                self.options.add_argument('window-size=1920x1080')
                self.options.add_argument('disable-extensions')
                self.webdriver = webdriver.Edge(options=self.options)

                self._get_chapters_links()

                print('********\nFound {} chapters. Select chapters for download. Options:'.format(
                    len(self.chapter_links.keys())))

                while True:
                    self._download_selection = input(
                        'Chapter number, range (ex 1-3), all or latest')

                    try:
                        if self._download_selection.lower() == 'latest':
                            print(sorted(list(self.chapter_links.keys()))[-1])

                        elif self._download_selection.lower() == 'all':
                            print(len(list(self.chapter_links.keys())))

                    except Exception as e:
                        print(e)

                self._get_image_links(title[0], url)

            def _get_chapters_links(self):

                self.webdriver.get(self.manga_url)
                wait = WebDriverWait(self.webdriver, 10)

                wait.until(EC.visibility_of_element_located((By.XPATH,
                                                       '//div[@class="series-contents"]//div['
                                                       '@class="js-readable-product-list"]')))

                _chap_list_cont = self.webdriver.find_element(By.XPATH, '//div[@class="series-contents"]//div['
                                                       '@class="js-readable-product-list"]')

                self.webdriver.execute_script('return arguments[0].scrollIntoView();',
                                              _chap_list_cont)

                while True:

                    try:
                        wait.until(EC.visibility_of_element_located(
                                    (By.XPATH, '//section[@class="read-more-container"]'
                                                '//button[@class="js-read-more-button"]'))).click()

                    except (TimeoutException, StaleElementReferenceException):
                        break

                chap_elems = self.webdriver.find_elements(
                                    By.XPATH, '//a[@class="series-episode-list-container"]')

                for c in chap_elems:
                    print(re.findall(r".*?\[[^\d]*(\d+)[^\d]*\].*", c.text))
                    print(c.get_attribute('href') + "\n")



                # self.tree = self.webdriver.find_element(by=By.TAG_NAME,
                #                                         value='body').text
                #
                # self.tree = ET.fromstring(self.tree)
                #
                # for e in self.tree.findall(
                #         '{http://www.w3.org/2005/Atom}entry'):
                #     title = e.find('{http://www.w3.org/2005/Atom}title').text
                #     title = re.findall(r"[0-9]+", title)
                #     url = e.find('{http://www.w3.org/2005/Atom}link').get('href')

                if title:
                    self.chapter_links.update({title[0]: url})

                print("########### chapters" + len(list(self.chapter_links.keys())))

            def _get_image_links(self, chapter_num, chapter_url):

                self.webdriver.get('view-source:' + chapter_url + '.json')
                self.content = self.webdriver.page_source
                self.chapter_content = self.webdriver.find_element(By.CLASS_NAME,
                                                                   'line-content').text
                self.chapter_data = json.loads(self.chapter_content)

                self.chapter_pages = \
                    self.chapter_data['readableProduct']['pageStructure']['pages']

                self._page_num = 0
                self._chapter = {}
                for page in self.chapter_pages:
                    if 'src' in page:
                        self._page_num = self._page_num + 1
                        self._page_link = page['src']

                        self._chapter.update({str(self._page_num): self._page_link})

                self.chapter_links.update({chapter_num: self._chapter})

            def _download_chapters(self):
                for c_num in self.chapter_links.values():
                    for c_page, c_links in c_num.items():
                        download(c_links, self.download_location + c_num + '\\' + c_page, 'jpeg')

        self.headless_browser = TonariScrapper()
        return self.headless_browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.headless_browser.webdriver.quit()


def main():
    setup_webdriver()

    with HeadlessBrowser() as headless:
        # print(headless.chapter_links['221'])

        print("ok")


if __name__ == '__main__':
    main()
