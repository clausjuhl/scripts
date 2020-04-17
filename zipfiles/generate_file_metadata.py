import csv
import hashlib
from pathlib import Path
from datetime import datetime

# FOLDER = Path(r'M:\Borgerservice-Biblioteker\Stadsarkivet\_DIGITALT ARKIV\ark_binary_store')
# STATUS_FILE = Path(r'M:\Borgerservice-Biblioteker\Stadsarkivet\_DIGITALT ARKIV\filestatus.csv')

FOLDER = Path(r'C:\Users\azkb075\00012315')
STATUS_FILE = Path(r'C:\_BITMAGASIN\zips\fileinfo.csv')
MEDIA = 'ARCHIVE_9'


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
    with open(STATUS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['modified', 'md5', 'media', 'path', 'filename', 'bytesize'])

        for obj in FOLDER.iterdir():
            obj_md5 = calculate_md5(obj)
            # get epoch-seconds as float from Path.stat() and convert to utc-datetime and finally to isoformat
            obj_ts = datetime.utcfromtimestamp(obj.stat().st_mtime).isoformat()
            obj_size = obj.stat().st_size
            obj_path = '/'.join(obj.parts[1:-1])  # exclude drive-info and filename
            writer.writerow([obj.name, obj_ts, obj_md5, obj_size, MEDIA, obj_path])


if __name__ == '__main__':
    main()
