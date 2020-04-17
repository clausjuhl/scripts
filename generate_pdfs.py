import img2pdf
from pathlib import Path


def main():
    def generate_pdf(folder_object, out_file_object):
        # folder_object, out_file_object and obj are Path-objects
        files = []
        for obj in folder_object.rglob('*.*'):
            if obj.suffix in ['.png', '.jpg', '.jp2', '.jpeg']:
                files.append(str(obj))  # img2pdf.convert requirement

        with open(out_file_object, "wb") as f:
            f.write(img2pdf.convert(files))

    for folder in Path('D:\16-0500_DK-82_Municipal-Censuses-1029-Jan-Dec-1915').iterdir():
        # for folder in Path.cwd():
        generate_pdf(Path(folder), Path(folder.stem + '.pdf'))
        print("generated " + folder.stem)


if __name__ == '__main__':
    main()
