# -*- coding: utf-8 -*-

from pathlib import Path
import shutil


IN = Path(r'C:\Users\azkb075\Downloads\PrebenRasmussen')
OUT = Path(r'C:\Users\azkb075\Downloads\PR_flat')

def main():
    # filenames = [idx.name for idx in list(OUT.glob('**/*.pdf'))]
    # filenames = []
    for idx in list(IN.glob('**/*.pdf')):
        filename = str(idx.parent) + "__" + str(idx.name)
        shutil.copy(idx, Path(OUT, filename))
        # man kan også gøre som nedenstående. copy2 bevarer metadata
        # Hvis man får Error 13, har man lavet en fejl med hvad der kopieres og hvorhen
        # det har ikke noget med rettigheder at gøre
        # shutil.copy2(idx, OUT)

if __name__ == '__main__':
    main()
