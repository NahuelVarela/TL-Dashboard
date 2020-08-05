# Amazing docs:
# https://google-auth.readthedocs.io/en/latest/reference/google.auth.transport.requests.html
#This file contains the logic for calling Appscript
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

import os
dirname = os.path.dirname(__file__)

import flask

SCOPES = ['https://www.googleapis.com/auth/script.projects',
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/userinfo.profile",
"https://www.googleapis.com/auth/userinfo.email",
"https://www.googleapis.com/auth/script.send_mail",
"https://www.googleapis.com/auth/plx",
"https://www.googleapis.com/auth/drive",
"openid"]

#We check if we are Prod or not
prod = os.environ.get("PROD","False")
if prod == "TRUE":
	CLIENT_SECRET = os.path.join(dirname, "credentials/prod_secret.json")
	redirect_url = 'https://tl-dashboard-hn2nnz4lda-ew.a.run.app/login/callback'
else:
	CLIENT_SECRET = os.path.join(dirname, "credentials/client_secret.json")
	redirect_url = 'https://127.0.0.1:5000/login/callback'

def authorize():
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
		CLIENT_SECRET,scopes=SCOPES)
	flow.redirect_uri = redirect_url
	#prompt='consent'
	authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='false',prompt='consent',)
	return authorization_url, state

def callback(state):
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
		CLIENT_SECRET,
		scopes=SCOPES,
		state=state)
	flow.redirect_uri = redirect_url
	authorization_response = flask.request.url
	flow.fetch_token(authorization_response=authorization_response)
	return flow.credentials

def userinfo(credentials):
	user_info_service = build(
	      serviceName='oauth2', version='v2',credentials=credentials)
	user_info = user_info_service.userinfo().get().execute()
	return user_info

def arrayToCread(info):
	credDict = {}
	credDict["client_id"] = info[0]
	credDict["client_secret"] = info[1]
	credDict["refresh_token"] = info[2]
	credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(info=credDict,scopes=SCOPES)
	credentials = refreshToken(credentials)
	return credentials

def refreshToken(credentials):
	import google.auth.transport.requests
	import requests
	request = google.auth.transport.requests.Request()
	credentials.refresh(request)
	return credentials
