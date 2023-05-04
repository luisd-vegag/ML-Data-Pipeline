import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile


def download_data(user, dataset, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(user + "/" + dataset, path=path)
    file = path + dataset + ".zip"
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(file))


if __name__ == "__main__":
    user = "jacksoncrow"
    dataset = "stock-market-dataset"
    path = "data/raw/"
    download_data(user, dataset, path)
