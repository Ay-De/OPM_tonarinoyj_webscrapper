import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
import re

from modules.webdriver import setup_webdriver
from modules.helpers import download


class HeadlessBrowser:

    def __enter__(self):

        class TonariScrapper:

            def __init__(self):

                self.manga_url = 'https://tonarinoyj.jp/episode/316190247048704205'
                self.tonari_url = 'https://tonarinoyj.jp/episode/'
                self.download_location = 'D:\OPM\\'

                self.chapter_links = {}

                self.options = Options()
                #self.options.add_argument('headless')
                self.options.add_argument('window-size=1920x1080')
                self.options.add_argument('disable-extensions')
                self.webdriver = webdriver.Edge(options=self.options)

                self.webdriver.set_network_conditions(
                        offline=False,
                        latency=1,  # additional latency (ms)
                        download_throughput= 28*500*1024,  # maximal throughput
                        upload_throughput=500*1024)  # maximal throughput

                self._get_chapters_links()

                print(f'********\nFound {len(self.chapter_links.keys())} '
                      f'chapters. Select chapters for download.\nOptions:')

                while True:
                    self._download_selection = input(
                        'Chapter number, range (ex 1-3), all or latest')

                    if self._download_selection.lower() == 'latest':
                        print(list(self.chapter_links.keys()))
                        #break

                    elif self._download_selection.lower() == 'all':
                        print(len(list(self.chapter_links.keys())))
                        #break

                    else:
                        try:
                            if int(self._download_selection):
                                print(int(self._download_selection))
                                #break

                        except ValueError:
                            try:
                                self._chap_range_lower, \
                                self._chap_range_upper = self._download_selection.split('-')

                                print('Chapters from {} to {} will be downloaded.'.format(
                                    self._chap_range_lower, self._chap_range_upper))
                                #break

                            except ValueError:
                                print('Invalid input. Example input for range: 1-5')


                self._get_image_links(title[0], url)

            def _get_chapters_links(self):

                self.webdriver.get(self.manga_url)
                wait = WebDriverWait(self.webdriver, 10)

                # wait.until(EC.visibility_of_element_located((By.XPATH,
                #                                        '//div[@class="series-contents"]//div['
                #                                        '@class="js-readable-product-list"]')))

               # _chap_list_cont = self.webdriver.find_element(By.XPATH, '//div[@class="series-contents"]//div['
                #                                       '@class="js-readable-product-list"]')

                _chap_list_cont = self.webdriver.find_element(By.XPATH,
                                                              '//button[@class="js-read-more-button"]')

                self.webdriver.execute_script('return arguments[0].scrollIntoView();',
                                              _chap_list_cont)

                _chapter_container_loaded = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                 '//span[@class="loading-text"]')))
                wait.until(lambda x: 'hidden' in _chapter_container_loaded.get_attribute('class'))

                while True:

                    try:
                        wait.until(EC.visibility_of_element_located(
                                    (By.XPATH, '//button[@class="js-read-more-button"]'))).click()

                    except (TimeoutException, StaleElementReferenceException):
                        break

                _chapters_available = self.webdriver.find_elements(By.XPATH,
                        '//*[@class=" episode" and not(contains(@class, "private episode"))] | '
                        '//*[@class="episode current-readable-product"]')

                _chapters_private = self.webdriver.find_elements(By.XPATH,
                        '//*[@class="private episode"]')

                regx = re.compile(r".*?\[[^\d]*(\d+)[^\d]*\].*")

                for c in _chapters_available:
                    c_num = regx.findall(c.text)
                    c_url = self.tonari_url + c.get_attribute('data-id')

                    if c_num:
                        self.chapter_links.update({int(c_num[0]): c_url})

                _all_chapters = sorted(list(self.chapter_links.keys()))

                _chapter_diffs = [x - y for (x, y) in zip(_all_chapters[1:], _all_chapters)]

                _idx_skipped_chapters = [i for i, v in enumerate(_chapter_diffs) if v > 1]

                if len(_idx_skipped_chapters) > 1:

                    #Add here logic to find multiple gaps of unpublished chapters
                    print(f'Note: Chapters {_all_chapters[_idx_skipped_chapters[0]] + 1} to '
                          f'{_all_chapters[_idx_skipped_chapters[0]]} are missing. '
                          f'Probably unpublished.')

                elif len(_idx_skipped_chapters) == 1:
                    if int(_idx_skipped_chapters[0]) > 1:
                        print(f'Note: Chapters {_all_chapters[_idx_skipped_chapters[0]] + 1} to '
                              f'{_all_chapters[_idx_skipped_chapters[0]]} are missing. '
                              f'Probably unpublished.')
                    else:
                        print(f'Note: Chapter {_all_chapters[_idx_skipped_chapters[0]]} is missing. '
                              f'Probably unpublished.')

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
