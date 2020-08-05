from flask_login import UserMixin


#Internal
import Database.database as database
import Oauth.serviceauth as serviceauth

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, creds):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.creds = creds

    @staticmethod
    def get(user_id):
        user_ref = database.getUser(user_id)
        if not user_ref:
            return None
        else:
            creds = serviceauth.arrayToCread(user_ref.get("creds"))
            user = User(
                id_=user_ref.get("ldap"), 
                name=user_ref.get("name"), 
                email=user_ref.get("email"), 
                profile_pic=user_ref.get("profile_pic"),
                creds=creds
            )
            return user

    @staticmethod
    def create(id_, name, email, profile_pic, creds):
        user = {
            "ldap":id_,
            "name":name,
            "email":email,
            "profile_pic":profile_pic,
            "creds":creds
            }
        database.creatUser(user)