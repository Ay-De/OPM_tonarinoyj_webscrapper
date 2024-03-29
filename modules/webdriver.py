import os
import requests
import re
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from tqdm import tqdm
from modules.helpers import unzip


def setup_webdriver():
    """This function will install the webdriver for selenium.
    It checks the installed Edge Chromium version, downloads and
    installs the fitting webdriver."""

    if os.path.isfile(os.getcwd() + '\\msedgedriver.exe'):
        try:
            _options = Options()
            _options.add_argument('headless')
            _webdriver = webdriver.Edge(options=_options)
            _webdriver.quit()

        except Exception as e:
            if 'WebDriver only supports'.lower() in e.msg.lower():
                print('Wrong webdriver version detected. '
                      'Downloading proper version...')

                proper_version = \
                    re.search('([0-9]+(\.[0-9]+)+)', e.msg)[0]

                _download_webdriver(proper_version)
                unzip('edgedriver_win64.zip', 'msedgedriver.exe')
                os.remove('edgedriver_win64.zip')

    else:
        chromium_dir = 'C:\Program Files (' \
                            'x86)\Microsoft\Edge\Application'
        version = _get_chromium_version(chromium_dir)
        _download_webdriver(version)
        unzip('edgedriver_win64.zip', 'msedgedriver.exe')
        os.remove('edgedriver_win64.zip')


def _get_chromium_version(chromium_dir):
    v = [d.path.split("\\")[-1] for d in os.scandir(chromium_dir) if
         d.is_dir() and d.path.split("\\")[-1].split(".")[0].isnumeric()]
    return sorted(v, reverse=True)[0]


def _download_webdriver(version):
    url = 'https://msedgedriver.azureedge.net/' + version + \
               '/edgedriver_win64.zip'
    response = requests.get(url, stream=True)

    download_size_bytes = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=download_size_bytes, unit='iB',
                        unit_scale=True)

    if response.status_code == 200:
        with open('edgedriver_win64.zip', 'wb') as f:
            for data in response.iter_content(1024):
                progress_bar.update(len(data))
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
        progress_bar.close()
