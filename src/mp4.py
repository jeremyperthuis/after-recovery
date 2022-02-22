import os
import logging
import sys
import ffmpeg
import shutil
from rich.progress import Progress
from pprint import pprint

class ProcessMP4:
    def __init__(self, dataframe):
        self.logger = logging.getLogger(__name__)
        #mute_third_party_logger()
        self.mp4_df = dataframe
        self.mp4_df = self.mp4_df.reset_index(drop=True)
        self.path = self.mp4_df['path'].iloc[0]
        self.get_metadatas()
        self.rename()

    def get_metadatas(self):
        self.mp4_df["new_filename"] = None
        with Progress() as progress:
            task1 = progress.add_task("Retrieve mp4 metadatas...", total=len(self.mp4_df))
            for index, row in self.mp4_df.iterrows():
                try:
                    probe = ffmpeg.probe(os.path.join(row["path"], row["filename"]+row["extension"]))
                    if "tags" in probe["format"].keys():
                        # pprint(probe["format"]["tags"])
                        print(probe["format"]["tags"]["artist"])
                        print(probe["format"]["tags"]["title"])
                        print("========================================")
                    # if "title" in probe["format"]["tags"].keys():
                    #     new_title = probe["format"]["tags"]["title"]
                    #     self.mp4_df.iloc[index, self.mp4_df.columns.get_loc('new_filename')] = new_title
                except ffmpeg.Error as e:
                    print(e.stderr, file=sys.stderr)
                    continue
                progress.update(task1, advance=1)

    def rename(self):
        self.mp4_to_rename_df = self.mp4_df[self.mp4_df["new_filename"].notnull()]
        with Progress() as progress:
            task_rename = progress.add_task("Rename mp4 files...", total=len(self.mp4_to_rename_df))
            # mp4 to rename
            for index, row in self.mp4_to_rename_df.iterrows():
                current_filename = os.path.join(row["path"], row["filename"]+row["extension"])
                new_filename = os.path.join(row["path"], row["new_filename"]+row["extension"])
                shutil.move(current_filename, new_filename)
                progress.update(task_rename, advance=1)