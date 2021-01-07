# YouTube-Video-Searcher
A django made web app used for searching top videos from youtube, in reverse chronological order

Fork the project on your repository, and clone it on your system

Setup a environment  using :  
1) pip install pipenv
2) pipenv install django
    
Run : python manage.py runserver 8001 
on your git. Make sure that you are in correct folder before running this command

Open other terminal and type the command :-   python manage.py process_tasks


Go to : localhost:8001/search/v1/tasks/ to get to the web app

Type your query on the search bar to get the latest videos in reverse chronological order

For now I have added the videos of cricket in the database. The background calls keep taking place for keyword cricket, and the web page displays the result of crickets irrespective of the query in search bar.
