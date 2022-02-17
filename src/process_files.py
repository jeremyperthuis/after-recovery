import os
import logging
import pandas as pd
from src.mp3 import mp3

class processFiles:
    def __init__(self, path):
        self.logger = logging.getLogger(__name__)
        self.files_df = pd.DataFrame()
        self.getfiles(path)
        self.mp3()

    def getfiles(self, path):
        numberOfFiles = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                filename, extension = os.path.splitext(f)
                if (os.path.isfile(fp)):
                    numberOfFiles += 1
                    self.files_df =self.files_df.append({"filename": filename, "path": fp, "extension": extension}, ignore_index=True)
    def mp3(self):
        m = mp3(self.files_df)
        m.get_metadatas()