from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from apiclient.http import MediaIoBaseDownload
# import zipfile
import zlib
from unlzw import unlzw
import json
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

class HistData():
    """
    Downloads json files of tweets between start_date and end_date
    (not inclusive of end_date) according to an interval
    """
    def __init__(self, start_date, end_date, interval=1):
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval

start_date = '2018-09-01'
end_date = '2018-09-02'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))
# mimeType='application/vnd.google-apps.folder' for folder
def download():
    response = service.files().list(q="name contains 'tag_data'").execute()
    file_ids_to_download = []
    for file in response.get('files', []):
        file_name = file.get('name')
        if file_name[:18] < 'tag_data' + end_date and file_name[:18] >= 'tag_data' + start_date:
            # file_ids_to_download.append(file.get('id'))
            download_request = service.files().get_media(fileId=file.get('id'))
            fh = io.FileIO(file_name, 'wb')
            downloader = MediaIoBaseDownload(fh, download_request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download {}".format(int(status.progress() * 100)))

def unzip(file_name):
    # if zipfile.is_zipfile(file_name):
    print("unzipping")
    # with zipfile.ZipFile(file_name, 'r') as zip_ref:
    #     zip_ref.extractall()
    with open(file_name, 'rb') as f: # Notice that I open this in binary mode
        file_content = f.read() # Read the compressed binary data
        decompressed_data = unlzw(file_content)
    counter = 0
    for line in decompressed_data:
        while counter < 10:
            print(json.loads(line))
            counter += 1
        break
        # print(repr(file_content[:30]))
        # decompressed = zlib.decompress(file_content, -15) # Decompress
    # with open(file_name[:-2], 'wb') as f:
    #     f.write(decompressed_data)
unzip('tag_data2018-09-01.json.Z')
