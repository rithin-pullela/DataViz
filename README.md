# DataViz
This is the backend for the Data Visulization Project, developed in flask and deployed in heroku.


# Env Setup:
python -m venv myenv

source myenv/bin/activate

pip install flask

# To run
python3 app.py

# Heroku deployment initial
pip install gunicorn

create Procfile 

pip3 freeze > requirements.txt

commit to git

heroku login

git push heroku main

heroku open


# Future deployments

heroku login

git push heroku main

heroku open
