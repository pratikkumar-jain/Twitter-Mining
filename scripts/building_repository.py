#!/usr/local/bin/python3

"""Script to build the repository from the extracted tweets"""

import json
import jsonpickle
import os
import sys
from zipfile import ZipFile


def main():
    """Unzip the compressed tweets"""
    #directory = os.fsencode("../data")
    root="../data/"
    for file in os.listdir(root):
        filename = os.fsdecode(file)
        if filename.endswith(".zip"):
            print(filename)
            with ZipFile(root+filename,"r") as zip_ref:
                zip_ref.extractall("../data")
    


if __name__ == '__main__':
    main()
