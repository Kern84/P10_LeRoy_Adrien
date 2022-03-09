[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)


# Project 10

SoftDesk wants to create an app that allow users to create various projects to follow technical issues, add users to specific projects, create issues within the projects and create comments within the issues.
We have to create the back-end app / API Rest using Django REST Framework.

## Technologies

- PYTHON

## Authors

Adrien LE ROY

## Configuration for program execution

The program was designed with Python 3.10.
Download the project file on GitHub : https://github.com/Kern84/P10_LeRoy_Adrien.git

Enter the commend lines in your terminal.
Go to the project folder, install and activate the virtual environment:
```bash
python3 -m venv env
source env/bin/activate
```

Install the packages needed for the project to work:
```
pip install -r requirements.txt
```

Launch the server:
```
python3 manage.py runserver
```

The local adress of the site:
http://127.0.0.1:8000

Deactivate the virtual environment when you are done viewing the project:
```
deactivate
```

## Postman documentation

https://documenter.getpostman.com/view/19829460/UVsFyTvf

## Users

This project has already three users created with different permissions.

- User 1 : superuser; email: adrien@email.fr; mot de passe: S3cret!1; first_name: adrien ; last_name: le roy. 
[Project creator, contributor]
- User 2 : email: lebron@email.fr; mot de passe: S3cret!2; first_name: Lebron; last_name: James. 
[Project contributor]
- User 3 : email: jordan@email.fr; mot de passe: S3cret!3; first_name: Michael; last_name: Jordan. 
[No Projects]