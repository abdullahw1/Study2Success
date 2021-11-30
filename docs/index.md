# Overview & Getting Started

## Description
This is a website app that intended to work as a student study helper, that target to support features like flashcards, notetaking,
learning from flashcards, pomodoro timer, personal To-Do list, and many more. Check out project [GitHub Repo](https://github.com/HoaTNNguyen/Study2Success)
for more information.


## QuickStart: Setting up server
This app is intend to serve multiple users with one server running, and each user will just signup on first use, and login
when using the created account. To set up a server, please follow the instructions below.

1. Clone the [GitHub Repo](https://github.com/HoaTNNguyen/Study2Success)

        % git clone https://github.com/HoaTNNguyen/Study2Success.git

2. Install latest [Python3.9](https://www.python.org/downloads/)

3. Go into the project main directory

        % cd Study2Success

4. It's recommended to create a virtual environment so we can make sure we have correct packages

        % pip3 install venv
        % python3 -m venv venv
        % source venv/bin/activate

5. Install all the packages from `requirements.txt`

        % pip3 install -r requirements.txt

6. Simply run the server now!

        % python3 app/run.py


## Contributors
- [@Hoa Nguyen](https://github.com/HoaTNNguyen)
- [@Ngan Ngo](https://github.com/RachelNgo)
- [@Jerusalem Ilag](https://github.com/jeruilag)
- [@Abdullah Waheed](https://github.com/abdullahw1)


## Directory structure

```
.
├── app                                         # Source code for applications
|   ├── myapp              
|   |   ├── static                              # CSS stylesheets, images, and javascript files needed for the app
|   |   ├── templates                           # contains all html files
|   |   |   ├── ...
|   |   ├── __init__.py                         # Set up flask and import library server
|   |   ├── forms.py                            # holds the code of all WTForms
|   |   ├── mdparser.py                         # holds the code helps extract markdown content into a list of Flashcards
|   |   ├── models.py                           # holds a list of Class that each representing the database table
|   |   ├── models_enum.py                      # Enum representing friend status in database
|   |   ├── models_methods.py                   # Functions returning all friends of a specified user
|   |   └── routes.py                           # hods all the routes of the app
|   └── run.py
├── docs                                        # Documentation folder (also used by [mkdocs](https://www.mkdocs.org) 
├── etc                                         # Contains all example files upload
├── mkdocs.yml                                  # Configuration file for mkdocs
└── requirements.txt                            # Dependency python packages
```

## Specifications
This is a project work in progress, for more information, please check out the [specifications document](Specification.md).

