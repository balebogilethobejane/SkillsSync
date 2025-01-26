import pyrebase
from dotenv import load_dotenv
import os


load_dotenv() 


firebaseConfig = {
  "apiKey":  os.getenv("APIKEY"),
  "authDomain": os.getenv("AUTHDOMAIN"),
  "databaseURL" : os.getenv("DATABASEURL"),
  "projectId": os.getenv("PROJECTID"),
  "storageBucket": os.getenv("STORAGEBUCKET"),
  "messagingSenderId": os.getenv("MESSAGINGSENDERID"),
  "appId": os.getenv("APPID"),
  "measurementId": os.getenv("MEASUREMENTID"),
  
}

firebase = pyrebase.initialize_app(firebaseConfig)



auth = firebase.auth()
db = firebase.database()

email = input("Enter email: ")
password = input("Enter password: ")

try:
   
    user = auth.create_user_with_email_and_password(email, password)
    print("User created successfully:", user)
except Exception as e:
    print("Error creating user:", e)




