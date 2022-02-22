import os
import logging
import shutil
from eyed3 import id3
from tinytag import TinyTag
from pprint import pprint
from rich.console import Console
from src.utils import convert_bytes, mute_third_party_logger

from rich.progress import Progress

class ProcessMP3:
    def __init__(self, dataframe):
        self.logger = logging.getLogger(__name__)
        mute_third_party_logger()
        self.mp3_df = dataframe
        self.mp3_df = self.mp3_df.reset_index(drop=True)
        self.path = self.mp3_df['path'].iloc[0]

        self.get_metadatas()
        self.rename()

    def get_metadatas(self):
        self.mp3_df["artist"] = None
        self.mp3_df["title"] = None
        with Progress() as progress:
            task1 = progress.add_task("Retrieve mp3 metadatas...", total=len(self.mp3_df))
            for index, row in self.mp3_df.iterrows():
                tag = id3.Tag()
                tag.parse(os.path.join(row["path"], row["filename"]+row["extension"]))
                artist = tag.artist
                title = tag.title

                if artist in ["", None, " "]:
                    artist = None
                if title in ["", None, " "]:
                    title = None
                    self.mp3_df.iloc[index, self.mp3_df.columns.get_loc('artist')] = artist
                self.mp3_df.iloc[index, self.mp3_df.columns.get_loc('title')] = title
                progress.update(task1, advance=1)

    def rename(self):
        self.mp3_to_rename_df = self.mp3_df[self.mp3_df["artist"].notnull() | self.mp3_df["title"].notnull()]
        self.mp3_to_ignore_df = self.mp3_df[self.mp3_df["artist"].isna() & self.mp3_df["title"].isna()]
        self.mp3_to_rename_df["new_filename"] = self.mp3_to_rename_df[["artist", "title"]].astype(str).agg(" - ".join, axis=1)

        renamed_path = os.path.join(self.path, "renamed")
        unknown_path = os.path.join(self.path, "unknown")
        self.mp3_to_rename_df["new_path"] = renamed_path
        self.mp3_to_ignore_df["new_path"] = unknown_path
        os.makedirs(renamed_path, exist_ok=True)
        os.makedirs(unknown_path, exist_ok=True)

        with Progress() as progress:
            task_rename = progress.add_task("Rename mp3 files...", total=len(self.mp3_to_rename_df) + len(self.mp3_to_ignore_df))
            # mp3 to rename
            for index, row in self.mp3_to_rename_df.iterrows():
                filename = row['new_filename']
                if "/" in row["new_filename"]:
                    filename = row["new_filename"].replace('/', '')

                current_filename = os.path.join(row["path"], row["filename"]+row["extension"])
                new_filename = os.path.join(row["new_path"], filename+row["extension"])
                shutil.move(current_filename, new_filename)
                progress.update(task_rename, advance=1)

            # mp3 to ignore
            for index, row in self.mp3_to_ignore_df.iterrows():
                current_filename = os.path.join(row["path"], row["filename"]+row["extension"])
                new_filename = os.path.join(row["new_path"], row["filename"]+row["extension"])
                shutil.move(current_filename, new_filename)
                progress.update(task_rename, advance=1)








