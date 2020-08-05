#########################
#### Oauth Blueprint ####
#########################

from flask import Flask, redirect, request, url_for, render_template, session, Blueprint
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

#Internal imports
from . import serviceauth
from Users.user import User
from Database import database

#State config used during auth flow
AUTH_STATE_KEY = 'auth_state'

#We define the blueprint for this Module
oauth_blueprint = Blueprint('oauth', __name__)

@oauth_blueprint.route("/login")
def login():
	authorization_url, state = serviceauth.authorize()
	session[AUTH_STATE_KEY] = state
	return redirect(authorization_url)

@oauth_blueprint.route("/login/callback")
def callback():
	state = session[AUTH_STATE_KEY]
	credentials = serviceauth.callback(state)
	
	user_info = serviceauth.userinfo(credentials)
	#This creates the user
	if user_info["verified_email"]:
		unique_id = user_info["id"]
		users_email = user_info["email"]
		picture = user_info["picture"]
		users_name = user_info["given_name"]
	else:
		return "User email not available or not verified by Google.", 400
		# by Google
	ldap = user_info["email"].split('@')[0]
	
	user = User(
		id_=ldap, name=users_name, email=users_email, profile_pic=picture, creds=credentials)
		# Doesn't exist? Add it to the database.
	if not User.get(ldap):
		arrayCreds = database.credToArray(credentials)
		User.create(ldap, users_name, users_email, picture, arrayCreds)
	# Begin user session by logging the user in
	login_user(user)
	return redirect("/")

@oauth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")