# Python standard libraries
import json
import os


# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template, session, Blueprint
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import requests
from flask_cors import CORS

# Internal Model imports
from Users.user import User
import Database.database

################
#### config ####
################

# Flask configuration
app = Flask(__name__,
			static_folder = "vue/dist/",
            template_folder = "vue/dist/",
            static_url_path='')
app.secret_key = '\x0eS\xed\xfb\xa2\xcf\x08\x8c\x95\t\xd5\x8f\x02\x1f\xd8t\x7f\xe6\xac\x8dG\xbb\x8bi'
app.config["TEMPLATES_AUTO_RELOAD"] = True

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

#We enable CORS
cors = os.environ.get("CORS_ENABLE","False")
if cors == 'True':
	print("CORS Enabled")
	CORS(app)
else:
	print("CORS disabled")

####################
#### blueprints ####
####################

from Oauth.router import oauth_blueprint
from Api.router import rest_api

app.register_blueprint(oauth_blueprint)
app.register_blueprint(rest_api)
# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



@app.route('/')
def hello_world():
    if current_user.is_authenticated:
        return render_template("index.html")

    else:
        print("Log")
        return '<a class="button" href="/login">Google Login</a>'
        
if __name__ == "__main__":
    prod = os.environ.get("PROD","False")
    if prod == "TRUE":
        app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    else:
        print("Adhoc")
        app.run(ssl_context="adhoc")
