import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

import io
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

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
        print('Downloading ID of image {0}'.format(status.progress()*100))

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

def image_detection():
    img = cv2.imread('images\ESP.JPG')
    # img = cv2.rotate(img ,cv2.ROTATE_180)
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    
    
    bfilter = cv2.bilateralFilter(gray,11,17,17)
    edged = cv2.Canny(bfilter , 30 , 200)
    plt.imshow(cv2.cvtColor(edged , cv2.COLOR_BGR2RGB))
    plt.show()
    # image gray conversion and filtering
    keypoints = cv2.findContours(edged.copy() , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    contours =  imutils.grab_contours(keypoints)
    contours = sorted(contours , key = cv2.contourArea , reverse=True)[:10]

    location = None
    contour_found = False
    cropped_image = img
    for contour in contours:
        approx = cv2.approxPolyDP(contour , 10 ,True) #can be set higher for more rougher approximation
        if len(approx) == 4 :
            location = approx
            contour_found = True
            break
    if contour_found:  
        mask = np.zeros(gray.shape , np.uint8)
        new_image = cv2.drawContours(mask , [location] , 0 ,255 ,-1)
        new_image = cv2.bitwise_and(img , img , mask = mask)
        (x,y) = np.where(mask == 255)
        (x1 , y1) = (np.min(x) , np.min(y))
        (x2 , y2) = (np.max(x) , np.max(y))
        cropped_image = gray[x1:x2+1 , y1:y2+1]
        plt.imshow(cv2.cvtColor(cropped_image , cv2.COLOR_BGR2RGB)) #why isnt this image grayscale?
        plt.show()
        res = cv2.rectangle(img , tuple(location[0][0]),tuple(location[2][0]),(150,0,255),3)#BGR
        plt.imshow(cv2.cvtColor(res , cv2.COLOR_BGR2RGB))
        plt.show()
    else:
        print('no contour found')
    return cropped_image

def number_detection(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    try:
        number = result[0][-2]
    except IndexError:
        print('number not found')
        number = ''
    return number



if __name__ == '__main__':
    #get_image('credentials.json' ,'drive' , 'v3' , scopes)
    print(number_detection(image_detection()))