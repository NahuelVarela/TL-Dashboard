#DB file

from google.cloud import firestore

#Get User
def getUser(user):
	""" Returns a User Document by ID (string) """
	db = firestore.Client()
	doc_ref = db.collection(u'users').document(user)
	user_ref = doc_ref.get()
	if user_ref.exists:
		user = {}
		user["ldap"] = user_ref.get("ldap")
		user["name"] = user_ref.get("name")
		user["email"] = user_ref.get("email")
		user["profile_pic"] = user_ref.get("profile_pic")
		user["creds"] = user_ref.get("creds")

		return user
	else:
		return False

def creatUser(user_dict):
	"""Creates a User if a dict is given."""

	db = firestore.Client()
	doc_ref = db.collection(u'users').document(user_dict["ldap"])
	result = doc_ref.set({
		"ldap":user_dict["ldap"],
		"name":user_dict["name"],
		"email":user_dict["email"],
		"profile_pic":user_dict["profile_pic"],
		"creds":user_dict["creds"]
		})

	return result

def credToArray(cred):
	""" Transofrms the Credentials obect into an array that can be uploaded to 
	Firestore """
	array = []
	array.append(cred.client_id)
	array.append(cred.client_secret)
	array.append(cred.refresh_token)
	return array