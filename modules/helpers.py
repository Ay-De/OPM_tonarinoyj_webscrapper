import os
import requests
from time import sleep
from zipfile import ZipFile


def unzip(zipfile: str, *args: [str], unziploc: [str] = None) -> None:
    """
    This helper function is used to unpack files from a zip file.
    :param zipfile: Path to zipfile to unpack.
    :param args: Files from the zipfile to be extracted. Default: All.
    :param unziploc: Path to the target extract location. Default: CWD.
    :return: None
    """
    with ZipFile(zipfile, 'r') as zip:
        if len(args) == 0:
            zip.extractall(path=unziploc)
        else:
            zip.extractall(path=unziploc, members=args)

    zip.close()


def download(url: str, filepath: str, filename: str) -> None:
    """
    Downloader helper function.
    :param url: Download link to the file.
    :param filepath: Target download location.
    :param filename: Target filename.
    :return: None
    """
    response = requests.get(url, stream=True)

    os.makedirs(filepath, exist_ok=True)

    filename = filepath + filename

    if response.status_code == 200:
        with open(filename, 'wb') as img:
            img.write(response.content)
            img.flush()
            os.fsync(img.fileno())

    else:
        print('Error downloading {} \n'.format(filename))

    sleep(0.2)
