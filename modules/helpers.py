from zipfile import ZipFile


def unzip(zipfile: str, *args: [str], unziploc: [str] = None) -> None:
    """
    This helper function is used to unpack files from a zip file.
    :param zipfile: Path to zipfile to unpack.
    :param args: Files from the zipfile to be extracted. Default: All
    :param unziploc: Path to the target extract location. Default: CWD.
    :return: None
    """
    with ZipFile(zipfile, 'r') as zip:
        if len(args) == 0:
            zip.extractall(path=unziploc)
        else:
            zip.extractall(path=unziploc, members=args)

    zip.close()
