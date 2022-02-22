import os
import logging
import shutil
import scandir
import time
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import track, Progress
from rich.spinner import Spinner

from src.mp3 import ProcessMP3
from src.mp4 import ProcessMP4

class processFiles:
    def __init__(self, sourcedir, destdir, group_by_extension):
        self.logger = logging.getLogger(__name__)
        dest = destdir if destdir != None else os.path.join(sourcedir,"_processed")
        self.config = {
            "src" : sourcedir,
            "dest" : dest,
            "group_by_extension": group_by_extension,
        }
        self.files_df = pd.DataFrame()
        #self.create_mock_data()
        # self.delete_mock_data()
        self.getfiles(sourcedir)

        if not self.files_df.empty:
            if group_by_extension:
                self.group_files_by_extension()
                self.delete_empty_folder()
            self.process_all()

    def getfiles(self, path):
        console = Console()
        with console.status("Scanning files..."):
            exclude = set(['renamed', 'unknown'])
            datalist = list()
            for dirpath, dirnames, filenames in os.walk(path):
                dirnames[:] = [d for d in dirnames if d not in exclude]
                for f in filenames:
                    filename, extension = os.path.splitext(f)
                    fullname = filename+extension
                    fullpathname = os.path.join(dirpath, fullname)
                    filesize = os.path.getsize(fullpathname)
                    if (os.path.isfile(fullpathname)):
                        #self.files_df =self.files_df.append({"filename": filename, "path": dirpath, "extension": extension, "size":filesize}, ignore_index=True)
                        datalist.append({"filename": filename, "path": dirpath, "extension": extension, "size":filesize})
            self.files_df = pd.DataFrame(datalist)

        if not self.files_df.empty:
            table = Table(title="")
            table.add_column("Type", justify="right", style="cyan", no_wrap=True)
            table.add_column("Number", style="magenta",justify="right")

            for extension in list(set(self.files_df["extension"].values.tolist())):
                amount = len(self.files_df[self.files_df["extension"] == extension])
                table.add_row(extension, str(amount))
            console = Console()
            console.print(table)
        else:
            print("empty files")

    def create_mock_data(self):
        import random
        os.makedirs("/home/perthuis/Documents/Projects/after-recovery/testdata", exist_ok=True)
        extension_list = [".mp3", ".csv", ".avi", ".c", ".h", ".mkv", ".class", ".wav"]
        for i in range(100):
            hash = random.getrandbits(128)
            folderpath = os.path.join(self.config["src"], str(hash))
            os.makedirs(folderpath, exist_ok=True)
            for i in range(50):
                filepath = os.path.join(folderpath,str(random.getrandbits(64)) + random.choice(extension_list))
                with open(filepath, 'a'):
                    os.utime(filepath, None)

    def delete_mock_data(self):
        shutil.rmtree("/home/perthuis/Documents/Projects/after-recovery/testdata")

    def delete_empty_folder(self):
        path_abs = self.config["src"]
        walk = list(os.walk(path_abs))
        for path, _, _ in walk[::-1]:
            if len(os.listdir(path)) == 0 and "_processed" not in path:
                os.rmdir(path)

    def group_files_by_extension(self):
        os.makedirs(self.config["dest"], exist_ok=True)
        for extension in list(set(self.files_df["extension"].values.tolist())):
            extensiondir = os.path.join(self.config["dest"], extension[1:])
            os.makedirs(extensiondir, exist_ok=True)
        print("Extension directories created.")

        with Progress() as progress:
            task_group = progress.add_task("Group files by extension...", total=len(self.files_df))
            for index, row in self.files_df.iterrows():
                current_file = os.path.join(row["path"], row["filename"]+row["extension"])
                dest_file = os.path.join(self.config["dest"], row['extension'][1:], row["filename"]+row["extension"])
                shutil.move(current_file, dest_file)
                self.files_df.iloc[index, self.files_df.columns.get_loc('path')] = os.path.join(self.config["dest"], row['extension'][1:])
                progress.update(task_group, advance=1)


    def process_all(self):
        ProcessMP3(self.files_df[self.files_df["extension"] == ".mp3"])
        #ProcessMP4(self.files_df[self.files_df["extension"] == ".mp3"])


""" TODO
- handle case where files have no extension
- handle case where multiple file have same new filename
"""
