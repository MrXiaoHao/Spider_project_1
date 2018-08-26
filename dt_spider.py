import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from urllib.parse import urlencode
from urllib.request import urlretrieve
import time
import os

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
}
def get_page_html(url,page):
    data = {
        "page": page
    }
    url = url + urlencode(data)
    try:
        response =requests.get(url,headers=headers)
        if response.status_code == 200:
            content =response.content
            return content
    except RequestException:
        get_page_html(url,page)
    time.sleep(1)

def parse_html(html):
    soup =BeautifulSoup(html,'lxml')
    image_lists = soup.find_all('img',{"class":"img-responsive lazy image_dta"})
    for img_url in image_lists:
        urls = img_url.attrs['data-original']
        save_url_images(urls)
        print("***保存图片成功***")
def save_url_images(img_url,file_path='images'):
    try:
        if not os.path.exists(file_path):
            print("文件不存在")
            os.mkdirs(file_path)
        split_url = img_url.split('/')#切割图片的url
        file_name = split_url.pop()
        path = os.path.join('images',file_name)
        urlretrieve(img_url,filename=path)
    except IOError as e:
        print("文件操作失败",e)
def main():
    page_url = "https://www.doutula.com/photo/list/?"
    for page in range(1,2):
        html = get_page_html(page_url,page)
        parse_html(html)

if __name__ == "__main__":
    main()