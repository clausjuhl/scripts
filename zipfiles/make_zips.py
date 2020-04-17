import os
import zipfile
from pathlib import Path

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

root = Path(r"D:\David_Sanchez\Aarhus Vejviser")
# zipper = zipfile.ZipFile(r'C:\Users\azkb075\developer\bitMagasin\AVID.AARS.7.1.zip', 'w', compression=compression)


def main():
    for folder in os.scandir(root):
        if "Aarhus Vejviser" in str(folder):
            #  print(str(folder))
            zipname = Path(folder).stem

            for cur_folder, sub_folders, files in os.walk(folder):
                zipper = zipfile.ZipFile('{}.zip'.format(zipname), 'w', compression=compression)
                for file in files:
                    # zipper.write(os.path.join(cur_folder, file))
                    zipper.write(os.path.join(cur_folder, file), os.path.relpath(os.path.join(folder, file), str(Path("D:\David_Sanchez\Aarhus Vejviser").joinpath(zipname))))
            zipper.close()

if __name__ == '__main__':
    main()
