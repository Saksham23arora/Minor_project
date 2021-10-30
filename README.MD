# Automatic bill generation system

This project was made by a team of 5 students in college to solve the problem of taking manual readings of differnt meters and then bill generation

## Installation and getting started

To install all the neccessary requirements run the following commands

```
pip install -r requirements.txt
```

## Setting up the virtual environment

> Note : It is recommended to setup a virtual environment and then run the program

```
py -m pip venv ./venv  #creating virtual environment
venv\Scripts\activate  #to activate the environment after creation
pip install -r requirements.txt # for installation of libraries

```

## For running the program

Run the main.py file using

```
python main.py
```

> Note : A client secret file has to be obatined from google cloud console and has to be placed in the root directory with the name 'credentials.json' to access the API's by google visit [Documentation of Google's API](https://developers.google.com/workspace/guides/create-credentials).

### Working

1. Firstly the `get_image()` function is called which downloades the latest meter reading image from Google drive (uploaded by ESP-32 microcontroller) and places the image in the images folder with name ESP.jpg
2. Then the `image_detection()` function is called which uses the open-cv library to do edge detection and returns a cropped image with just the reading
3. This cropped image is then passed to the `number_detection()` function which uses the [EasyOCR](https://github.com/JaidedAI/EasyOCR) library to detect the reading and convert the reading into a string.

### Issues

- [x] Get image from google drive
- [ ] Fix the working of `image_detection()` and `number_detection()` functions

