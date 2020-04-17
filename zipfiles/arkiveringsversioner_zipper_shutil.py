from pathlib import Path
import os
import zipfile
import hashlib


try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
    # compresslevel = 9 - being introduced in 3.7
except:
    compression = zipfile.ZIP_STORED
    # compresslevel = None - being introduced in 3.7


INPUT_PATH = r'C:\Users\azkb075\00012976'
OUTPUT_FOLDER = r'C:\Users\azkb075'
OUT_FILE_STEM = '00012976'
MAX_BYTE_SIZE = 4294967296  # 4GB


def calculate_md5(filepath, block_size=256*128, hex=True):
    '''
    Block size directly depends on the block size of your filesystem
    to avoid performances issues. Here I have blocks of 4096 octets
    (equals 32768 bytes, which is default in NTFS, used in Windows)
    '''
    md5 = hashlib.md5()
    with open(filepath,'rb') as f: 
        for chunk in iter(lambda: f.read(block_size), b''): 
            md5.update(chunk)

    return md5.hexdigest() if hex else md5.digest()


def invalid_zipfile(filepath):
    '''
    Checks both the zip-container and the files within.
    Returns None if valid, else some error-string
    '''
    # Test if the filepath points to a .zip-file with a valid container
    try:
        zfile = zipfile.ZipFile(filepath, 'r')
    except zipfile.BadZipfile:
        return "%s no a valid zip-container" % filepath

    # Test the content of each file in the zip-archive
    return zfile.testzip()


def generate_zipfile(in_filepaths, root_path, out_filepath):
    '''
    in_filepaths must be a list of complete filepaths as strings
    root_path is used to avoid representing the full filepaths inside the zip-archive
    out_filepath is the full path, incl. filename, of the generated zip-archive
    '''
    with zipfile.ZipFile(out_filepath, mode='w', compression=compression) as archive:
        print('Generating zipfile: ' + out_filepath)
        for path in in_filepaths:
            # Produces a correct - and less than full - path of each file
            # Eg. 00011744\A\117441\BRUGSVEJLEDNING.TIF
            archive.write(path, os.path.relpath(path, root_path))


def main():
    archive_files = []
    current_size = 0
    current_counter = 1
    for root, folders, files in os.walk(INPUT_PATH):
    
        for filestring in files:
            full_path = os.path.join(root, filestring)
            size = os.stat(full_path).st_size

            # If sum larger than max-byte-size, generate zipfile of archive_files
            if (current_size + size > MAX_BYTE_SIZE):
                # generate zip-file with the current batch of files
                filename =  OUT_FILE_STEM + '_' + str(current_counter) + '.zip'
                filepath = os.path.join(OUTPUT_FOLDER, filename)

                generate_zipfile(archive_files, r'C:\Users\azkb075', filepath)
                invalid = invalid_zipfile(filepath)
                if invalid:
                    print(invalid)
                archive_files = []  # reset filelist
                current_size = 0  # reset size of current files
                current_counter += 1  # bump counter
            else:
                current_size += size

            # Append current file to archive_files no matter what
            archive_files.append(full_path)

    if archive_files:
        filename =  OUT_FILE_STEM + '_' + str(current_counter) + '.zip'
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        generate_zipfile(archive_files, r'C:\Users\azkb075', filepath)


if __name__ == '__main__':
    main()
