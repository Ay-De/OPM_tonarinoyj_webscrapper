import requests
#from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50'
}

def main():


    url = 'https://tonarinoyj.jp/episode/13932016480028985383'
    xhr_url = 'https://tonarinoyj.jp/atom/series/13932016480028984490'

    options = Options()
    #options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    #options.add_argument('window-size=3840x2160')


    driver = webdriver.Edge(options=options)

    driver.get(url)
    next2 = driver.find_element(by=By.XPATH, value="//span[@class='viewer-btn-expand js-viewer-btn-expand']")
    next2.click()

    try:
        while True:
            next = driver.find_element(by=By.XPATH, value="//a[@class='page-navigation-forward rtl js-slide-forward']")
            next.click()
            time.sleep(0.5)
            #print(next.get_attribute('class'))
    except:
        print('end of comic')

    next.click()
    time.sleep(0.5)
    next.click()

    time.sleep(1)
    driver.get_screenshot_as_file('test.png')
    img = driver.get_screenshot_as_png()
    img = np.asarray(Image.open(io.BytesIO(img)))

    print(img.shape)
    with Image.open('test.png') as i:
        print(np.asarray(i).shape)

    plt.imshow(img)
    plt.imshow(i)
    plt.show()
    driver.quit()

    print("asd")
    with requests.Session() as sess:
        sess.get(url, headers=headers)
        response = sess.get(xhr_url, headers=headers, params={'free_only': '1'})
        print(response.content)
#
#     session = HTMLSession()
#     response = session.get(url)
#     response.html.render()
#     print(response.html.html)
#
#     #  soup = bs(response.text, 'html.parser')
#
#     # image_viewer = soup.find('div', attrs={'id': 'content', 'class': 'content-horizontal'})
#     # image_viewer2 = image_viewer.find('div', attrs={'class': 'content-inner scroll-horizontal js-horizontal-viewer'})
#
#     #   for n in image_viewer2:
#     #        print(n)
#     #  image_viewer3 = image_viewer2.find('div', attrs={'class': 'image-container js-viewer-content selectable is-spread'})
#
#     options = Options()
#     options.add_argument('--headless')
#     #driver = webdriver.Chrome(chrome_binary='chromedriver.exe', chrome_options=options)
#     driver.get(url)
#     page = driver.page_source
#     driver.quit()
#
#     soup = bs(page, 'html.parser')
#
#     image_viewer = soup.find('div', attrs={'id': 'content', 'class': 'content-horizontal'})
#     image_viewer2 = image_viewer.find('div', attrs={'class': 'content-inner scroll-horizontal js-horizontal-viewer'})
#
#     image_viewer3 = image_viewer2.find('p', attrs={'class': 'page-area js-page-area align-left'})
#
#     for i in image_viewer3:
#         print(i)
#         print('\n')
#
#     # test = soup.find_all('p', ['page-area js-page-area align-left', 'page-area js-page-area align-right'])
#     # select = ['image_viwer.p.page-area js-page-area align-left']
#
#     # for img in image_viewer.findAll('p', attrs={'class': 'page-area js-page-area align-left'}):
#     #    img_url = img.get('src')
#     #    print(img_url)
#
#     print("asd")
#
#   #  response = requests.get(website, headers=headers)
#
#   #  soup = bs(response.text, 'html.parser')
#
#    # image_viewer = soup.find('div', attrs={'id': 'content', 'class': 'content-horizontal'})
#    # image_viewer2 = image_viewer.find('div', attrs={'class': 'content-inner scroll-horizontal js-horizontal-viewer'})
#
#  #   for n in image_viewer2:
# #        print(n)
#   #  image_viewer3 = image_viewer2.find('div', attrs={'class': 'image-container js-viewer-content selectable is-spread'})
#
#     options = Options()
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(chrome_binary='chromedriver.exe', chrome_options=options)
#     driver.get(url)
#     page = driver.page_source
#     driver.quit()
#
#     soup = bs(page, 'html.parser')
#
#     image_viewer = soup.find('div', attrs={'id': 'content', 'class': 'content-horizontal'})
#     image_viewer2 = image_viewer.find('div', attrs={'class': 'content-inner scroll-horizontal js-horizontal-viewer'})
#
#     image_viewer3 = image_viewer2.find('p', attrs={'class': 'page-area js-page-area align-left'})
#
#     for i in image_viewer3:
#         print(i)
#         print('\n')
#
#     #test = soup.find_all('p', ['page-area js-page-area align-left', 'page-area js-page-area align-right'])
#     #select = ['image_viwer.p.page-area js-page-area align-left']
#
#     #for img in image_viewer.findAll('p', attrs={'class': 'page-area js-page-area align-left'}):
#     #    img_url = img.get('src')
#     #    print(img_url)

    print("asd")

if __name__ == '__main__':
    main()