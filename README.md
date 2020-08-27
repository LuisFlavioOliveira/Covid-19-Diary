# Covid-19 Diary

Covid-19 Diary is a web application that allows users to keep track 
of their movements in zones where the Covid-19 is highly active.




The application enables the user to write down all the locations 
where he/she has been in the last days, all the people he/she has seen 
and using a scale, how the user was feeling in that specified day/hour 
(Good, Not so well or Sick).




The Covid-19 Diary will provide a complete diary, where you will be 
able to follow all your movements and help in the fight against the 
Coronavirus. The idea is simple: if you are infected, you can get in 
touch with the people you have had contact with and the places you have 
been to inform them that you are infected. On the other hand, if, 
eventually, you know that someone with whom you have recently been 
infected or that one of the places where you have been having been found to
 have a case of Covid-19, you can take precautions as if you were 
infected. The idea is exactly to help us to prevent the spread of the 
virus through simple actions that depend only on ourselves, without 
governments or companies watching us.




The web application also provides the latest information and 
statistics about the Covid-19 in your country, as the total number of 
active cases, the number total of deaths and new deaths in the current 
day, as well the total of recovered.
The page also displays a chart with the number of total deaths and active cases, like that the user can follow the evolution of the Covid-19 in their region. All this information is provided and update in real-time 
by an API from Johns Hopkins Coronavirus Resource Center.


## The methodology 

The idea was to create a web application using the paradigm MVC 
(Model View Controller) where the "Model" stands for the data of the 
tables and the rows that are inside of the database I created with 
SQLite3 (i.e. users, password, diary, etc.).




The "View" determines what the user sees, in that case, 
these are the templates, the HTML files that display forms for the user 
to fill out, the tables that show all the diary entries and all the 
other visual aspects.




Finally, the "Controller" is represented by the application.py, it's 
the logic that connects the "Model" and the "View"  with. The controls
 is responsible to make database queries to finance.db by running SQL 
queries and pass these data to a template, to a view to 
determine what it is the user is going to see when they perform 
actions with the application, and also what connects the API with the 
front-end.

## Specifications about the source code 

I gave a lot of emphasis on the security aspect working on this web 
application. I've implemented security checks in both front-end (HTML 
forms with required and patterns) and back-end (if statements to protect
 against bad users) to avoid any SQL injection or other types of 
attacks.




To register, the user must provide a username with max-length of 16 
characters and only with alphanumeric characters and some pre-defined 
special characters. The e-mail must follow a defined pattern also that respects RFC 5322 Official Standard.
The password must have more than 8 characters and contain at least one 
number, one uppercase and lowercase letter, and one special character.




The passwords are stored using hashing and salting methods, guaranteeing they are not stored in plain-text.




The API is contacted by a function inside the file helpers.py, that 
calls one of the provides endpoints to get in real-time the latest 
statistics from the spread of Covid-19 in a selected country.

## Tools 

* Python 3.8.3 - The Back-End
* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - The Web Framework used
* [Jinja](https://www.palletsprojects.com/p/jinja/) - Template Engine
* [SQLite](https://www.sqlite.org/index.html) - Database Engine
* [BootStrap](https://getbootstrap.com/) - Front-End component (Menu)
* [API](https://covid19api.com/) - Covid19API


## Screenshots

![Index](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Index%20page.png)
![Register](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Sign%20Up.png)
![HomePage](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/HomePage.png)
![Search Result](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Search%20page.png)
![Write](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Write.png)
![Diary](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Diary.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

You will need Python 3.x and the following libraries and packages. Type commands in terminal to install:

`pip install flask`

`pip install flask_session`

`pip install sqlite3`

`pip install cs50`

To use the API, you'll need to read the documentation on [API COVID19](https://covid19api.com/)

### Installing

A step by step series of examples that tell you how to get a development env running

Download all files into a folder. Ensure that all imported libraries in `app.py` and `helpers.py` are 
installed on your machine or virtual environment.

Run the program on your machine or virtual environment.

```
flask run
```

## License / Copyright

* Completed as my final project of Harvard CS50 Curriculum
* This project is licensed under the MIT License.
