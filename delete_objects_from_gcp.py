import subprocess
from pathlib import Path
import csv

"""Delete online digital representations of resources.

This script works in WSL. Use "gcloud auth login" before running the script
The object_file contains a list of resourceId's. Use the same file when creating an update-job in SAM
"""


object_folder = "/mnt/c/Users/azkb075/local_developer/Backup-search"
object_file = "QA_20200701_online_representations_but_privacy_restricted.csv"

def main():
    suffixes = ["_l.jpg", "_m.jpg", "_s.jpg"]
    with open(Path(object_folder, object_file)) as ifile:
        reader = csv.reader(ifile)
        reader.__next__()
        for id_ in reader:
            for suffix in suffixes:
                # print(f"{id_[0]}{suffix}")
                # print(f"gsutil rm gs://openaws-access/{id_[0]}{suffix}")
                subproc = subprocess.Popen(f"gsutil rm gs://openaws-access/{id_[0]}{suffix}", shell=True, stdout=subprocess.PIPE)
                subprocess_return = subproc.stdout.read()
                print(subprocess_return)


if __name__ == "__main__":
    main()
