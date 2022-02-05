from filestack import Client
from dotenv import load_dotenv
import os


class FileSharer:

    def __init__(self, filepath):
        self.filepath = filepath
        load_dotenv()
        self.api_key = os.environ.get('API_KEY')

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url
