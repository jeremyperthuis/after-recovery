import logging

class mp3:
    def __init__(self, dataframe):
        self.logger = logging.getLogger(__name__)
        self.mp3_df = dataframe


    def get_metadatas(self):
        pass