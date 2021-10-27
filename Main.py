import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

import io

scopes = ['https://www.googleapis.com/auth/drive']
def get_image(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
    



    text_file_id = '1M1_8Zl8C4s6Yo9LVnPIvO1ZAOpfqYa9H' 
    request=service.files().get_media(fileId=text_file_id)
    fh=io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done=False
    while not done:
        status,done = downloader.next_chunk()
        print('Downloading text file {0}'.format(status.progress()*100))

    fh.seek(0)
    # print("this is the data " + str(fh.read()))
    fh = str(fh.read())
    fh = fh[2:fh.__len__()-1] #string slicing
    #print(fh)
    file_id = fh
    file_name = 'ESP.JPG'    
    request=service.files().get_media(fileId=file_id)

    fh=io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done=False

    while not done:
        status,done = downloader.next_chunk()
        print('Downloading image {0}'.format(status.progress()*100))

    fh.seek(0)
    with open(os.path.join('./images',file_name),'wb') as f:
        f.write(fh.read())
        f.close()
    return service        

if __name__ == '__main__':
    get_image('credentials.json' ,'drive' , 'v3' , scopes)