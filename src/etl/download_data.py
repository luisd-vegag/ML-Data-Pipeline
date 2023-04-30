import os
import urllib.request

def download_data(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    urllib.request.urlretrieve(url, path)

if __name__ == '__main__':
    url = 'https://www.kaggle.com/jacksoncrow/stock-market-dataset/download'
    path = 'data/raw/stock-market-dataset.zip'
    download_data(url, path)
