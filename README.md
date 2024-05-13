# Job Hunters
## T-220-VLN2 Verklegt námskeið 2
### _Group 30_
___
### University of Reykjavík, department of computer science
#### Students: Hafsteinn Már Heimisson, Mikael Elí Stefánsson
___
\
A project built for T-220-VLN2, spring semester 2024. The project implements a job posting board
with a multi step application form. The companies can add details about the company along with cover image and logo and about the jobs
that they list. The job seeking users can update their name and profile picture and apply to jobs, after which
they can check the status of the applications.



### Instructions for running 
To run this program you will need to install the dependencies first, be it in a virtual env, container or
on a system level

\
You can install them by running the following in your environment of choice

```
  pip install -r requirements.txt
```
\
Next you will need to run django migrations to set up the database with the following command

```
  python manage.py migrate
```
\
By default it will create an sqlite database in the app directory, this can be overridden by setting up your own
database connection in settings.py and then re-running the migration.

>>>__NOTE TO INSTRUCTOR: In the version we sent to you our cloud database credentials are already active in settings.py.__

\
The migration imports a lot of data for demonstration purposes. In this process it creates users that you might want to
login as while testing the system.

We provide a command to conveniently set the password for all users, strictly for testing of course.

```
python manage.py change_all_passwords PASSWORD  // Where PASSWORD is a string that you want to put as all users password
```

