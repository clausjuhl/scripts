from pathlib import Path
from typing import List, Dict
import shutil
import csv
import hashlib

# IN = Path(r"C:\Users\azkb075\Downloads\PrebenRasmussen")
# OUT = Path(r"C:\Users\azkb075\Downloads\PrebenRasmussen_Emnesamling")
IN = Path(r"/Users/cjk/Downloads/Preben Rasmussen Emnesamling - klar til SAM")
OUT = Path(r"/Users/cjk/Downloads/PrebenRasmussen_Emnesamling_A-Militær")


def main():
    pdfs: List[Dict] = []

    for pdf in list(IN.glob("**/*.pdf")):
        if Path(OUT / pdf.name).exists():
            print(f"Already exists: {pdf.name}")
            pdf = pdf.rename(Path(pdf.parent) / f"2_{pdf.name}")
        checksum: str = ""
        with open(pdf, "rb") as f:
            bytes = f.read()  # read file as bytes
            checksum = hashlib.md5(bytes).hexdigest()
        shutil.copy2(pdf, Path(OUT, pdf.name))
        pdfs.append(
            {
                "serie": str(pdf.parent),
                "checksum": checksum,
                "filename": pdf.name,
            }
        )

        # for idx in pdfs:
        #     print(f"{idx['filename']}: {idx['checksum']}")

    with open(
        OUT / "pr_metadata.csv", "w", encoding="utf-8", newline=""
    ) as ofile:
        fieldnames = ["serie", "checksum", "filename"]
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
        for d in pdfs:
            writer.writerow(d)


if __name__ == "__main__":
    main()
