import zipfile
import csv
from pathlib import Path
from datetime import datetime

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
    # compresslevel = 9
except:
    compression = zipfile.ZIP_STORED
    # compresslevel = None

# ARCHIVE_FOLDER = Path(r'M:\Borgerservice-Biblioteker\Stadsarkivet\_DIGITALT ARKIV\ark_binary_store')
OUTPUT_FOLDER = Path(r'C:\_BITMAGASIN\zips')
# STATUS_FILE = Path(r'M:\Borgerservice-Biblioteker\Stadsarkivet\_DIGITALT ARKIV\filestatus.csv')
MAX_BYTE_SIZE = 4294967296  # 4GB

ARCHIVE_FOLDER = Path(r'C:\Users\azkb075\temporary\skattemandtalslister')
STATUS_FILE = Path(r'C:\_BITMAGASIN\zips\fileinfo.csv')

def get_current_files():
    # returns a dict with unique filenames as keys and last_modified_utc_ts as values
    out = {}
    with open(STATUS_FILE) as ifile:
        reader = csv.reader(ifile)
        reader.__next__()
        for row in reader:
            out[row[4]] = row[0]
    return out

def generate_zipfile(filelist):
    # filelist must be array of Path-objs
    filename = datetime.utcnow().isoformat().replace(':', '').replace('.', '')
    with zipfile.ZipFile(OUTPUT_FOLDER / '{}.zip'.format(filename), mode='w', compression=compression) as archive:
        for path_obj in filelist:
            archive.write(path_obj)

def main():
    current_size = 0
    current_files = get_current_files()
    archive_files = []

    for obj in ARCHIVE_FOLDER.iterdir():
        if obj.is_file:
            # get epoch-seconds as float from Path.stat() and convert to utc-datetime and finally to isoformat
            ts = datetime.utcfromtimestamp(obj.stat().st_mtime).isoformat()
            size = obj.stat().st_size
            name = obj.name

            # If obj is new or modified
            if (name not in current_files) or ts != current_files.get(name):
                
                # If sum larger than max-byte-size, generate zipfile and reset size and filelist
                if (current_size + size > MAX_BYTE_SIZE):
                    if not archive_files:
                        print("Error. File too large: " + name)
                    else:
                        generate_zipfile(archive_files)
                        archive_files = []  # reset filelist
                        current_size = 0  # reset size
                else:
                    archive_files.append(obj)
                    current_size += size
    
    if archive_files:
        generate_zipfile(archive_files)


if __name__ == '__main__':
    main()
