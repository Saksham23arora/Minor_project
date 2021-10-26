import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

import io

scopes = ['https://www.googleapis.com/auth/drive']
def Create_Service(client_secret_file, api_name, api_version, *scopes):
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
    
    # page_token = None
    # while True:
        
    #     response = service.files().list(q="not name contains 'hello'",
    #                                         spaces='drive',
    #                                         fields='nextPageToken, files(id, name)',
    #                                         pageToken=page_token).execute()
    #     print (response.get('files', []))
    #     for file in response.get('files', []):
    #         # Process change
    #         print ('Found file: {0} ({1})'.format(file.get('name'), file.get('id')))
    #     page_token = response.get('nextPageToken', None)
    #     if page_token is None:
    #         break
    file_ids = ['1zvsQA9fVHwM9ZStz3y-4sbhfdOEtgy0U']
    file_names = ['ESP.JPG']

    for file_id , file_name in zip(file_ids,file_names):
        request=service.files().get_media(fileId=file_id)

        fh=io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)

        done=False

        while not done:
            status,done = downloader.next_chunk()
            print('Download progress {0}'.format(status.progress()*100))

        fh.seek(0)
        with open(os.path.join('./images',file_name),'wb') as f:
            f.write(fh.read())
            f.close()
    return service        


Create_Service('credentials.json' ,'drive' , 'v3' , scopes)