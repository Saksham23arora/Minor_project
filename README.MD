# Automatic bill generation system

This project was made by a team of 5 students in college to solve the problem of taking manual readings of differnt meters and then bill generation

## Installation and getting started

To install all the neccessary requirements run the following commands

```
pip install -r requirements.txt
```

## Setting up the virtual environment

> It is recommended to setup a virtual environment and then run the program

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

> Note : a client secret file has to be obatined from google cloud console and has to be placed in the root directory with the name 'credentials.json' to access the API's by google visit [Documentation of Google's API](https://developers.google.com/workspace/guides/create-credentials).
