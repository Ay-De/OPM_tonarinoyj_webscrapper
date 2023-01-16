import os
from tqdm import tqdm
import requests
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import xml.etree.ElementTree as ET
import re


class SetupWebdriver:
    def __init__(self):

        if os.path.isfile(os.getcwd() + '\\msedgedriver.exe'):
            print('webdriver already exists')

            try:
                webdriver.Edge()
            except Exception as e:
                if 'WebDriver only supports' in str(e.args):
                    proper_version = re.search('([0-9]+(\.[0-9]+)+)', str(e.args))[0]
                    self.download_webdriver(proper_version)
                    self.unzip()
        else:
            self.chromium_dir = 'C:\Program Files (x86)\Microsoft\Edge\Application'
            self.version = self.get_chromium_version(self.chromium_dir)
            self.download_webdriver(self.version)
            self.unzip()
        
    def get_chromium_version(self, chromium_dir):
        v = [d.path.split("\\")[-1] for d in os.scandir(chromium_dir) if d.is_dir() and d.path.split("\\")[-1].split(".")[0].isnumeric()]
        return sorted(v, reverse=True)[0]

    def download_webdriver(self, version):
        self.url = 'https://msedgedriver.azureedge.net/' + version + '/edgedriver_win64.zip'
        response = requests.get(self.url, stream=True)

        download_size_bytes = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=download_size_bytes, unit='iB', unit_scale=True)

        with open('edgedriver_win64.zip', 'wb') as f:
            for data in response.iter_content(1024):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

    def unzip(self):
        with ZipFile('edgedriver_win64.zip', 'r') as zip:
            zip.extract('msedgedriver.exe')
        zip.close()

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
                #pattern = re.compile(r"[0-9]+", re.IGNORECASE)
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

    SetupWebdriver()

    with HeadlessBrowser() as headless:

        print(headless.chapters['1'])

        print("ok")


if __name__ == '__main__':
    main()