# Tweet-It

A social network app that allows users to make posts, follow other users, and “like” posts.

### Back-end

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

### Front-end

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)

| License | GPLv3 |
| :-----: | :---: |


# Key Functionalties

* A social network app that allows users :hear_no_evil: to make posts, follow other users, and “like” :heartbeat: posts.

* Signed-in users are able to create a new text-based post by typing into a text box and then clicking a button to submit it .

* The “All Posts” link in the navigation bar send the user to a page where they may see all of the posts from all users, in chronological order.

* In profile detail page you can see the user's total number of followers as well as the number of individuals he or she follows and a user As a matter of course can't follow onself.

* The “Following” link in the navigation bar should send the user to a page where they can see all of the posts made by the individuals they are following.

* Users are able to edit any of their own postings by clicking a "Edit"  button or link.



Settings
--------

Moved to
[settings](/project4/settings.py).

## QuikStart

- Create a Virtual environment

    `python3 -m venv .venv`

- Activate the Virtual environment

    `source .venv/bin/activate`

- Install required packages

    `pip3 install -r requirements.txt`

- Run Migration for Models

    `python3 manage.py migrate --settings=mysite.settings.local`

- Start Development Server

    `python3 manage.py runserver --settings=mysite.settings.local`


Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you\'ll see a message that your account cerates succesfully. 

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

