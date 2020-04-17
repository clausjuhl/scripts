# This works and is usable if you want to only zip certain files og filetypes in a folder

import os
import zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

zipper = zipfile.ZipFile(r'C:\Users\azkb075\developer\bitMagasin\AVID.AARS.7.1.zip', 'w', compression=compression)

def main():
    for folder, subfolders, files in os.walk(r'C:\Users\azkb075\AVID.AARS.7.1'):
    
        for file in files:
            # if file.endswith('.TIF'):
            # Produces a less than full path of each file, eg. 00011744\A\117441\BRUGSVEJLEDNING.TIF
            zipper.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), 'C:\\Users\\azkb075'))
                
            # Produces full tree-structure for the files, eg. C:\Users\azkb075\00011744\A\117441\BRUGSVEJLEDNING.TIF
            # zipper.write(os.path.join(folder, file))
    
    zipper.close()

if __name__ == '__main__':
    main()
