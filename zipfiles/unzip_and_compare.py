import csv
import hashlib
from pathlib import Path
import os

ZIPPED = r'C:\Users\azkb075\developer\bitMagasin\00012315.zip'
ORIGINAL = r'C:\Users\azkb075\00012315'

def unzip(zipped=ZIPPED):


def calculate_md5(path, block_size=256*128, hr=True):
    '''
    Block size directly depends on the block size of your filesystem
    to avoid performances issues. Here I have blocks of 4096 octets
    (equals 32768 bytes, which is default in NTFS, used in Windows)
    '''
    md5 = hashlib.md5()
    with open(path,'rb') as f: 
        for chunk in iter(lambda: f.read(block_size), b''): 
            md5.update(chunk)
    if hr:
        return md5.hexdigest()
    return md5.digest()

def main():

    hashtable = {}
    # generate md5 for original file
    # unzip zipped file
    # compare md5 for unzipped file with original md5
    for root, folders, files in os.walk(ORIGINAL):

        for filestring in files:
            full_path = os.path.join(root, filestring)
            rel_path = os.path.relpath(full_path, ORIGINAL)
            hashtable[rel_path] = calculate_md5()

    
if __name__ == '__main__':
    main()
