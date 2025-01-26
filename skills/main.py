import pyrebase
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Firebase configuration from .env file
firebaseConfig = {
    "apiKey": os.getenv("APIKEY"),
    "authDomain": os.getenv("AUTHDOMAIN"),
    "databaseURL": os.getenv("DATABASEURL"),
    "projectId": os.getenv("PROJECTID"),
    "storageBucket": os.getenv("STORAGEBUCKET"),
    "messagingSenderId": os.getenv("MESSAGINGSENDERID"),
    "appId": os.getenv("APPID"),
    "measurementId": os.getenv("MEASUREMENTID"),
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Firebase Authentication and Database references
auth = firebase.auth()
db = firebase.database()

# User input for email and password
email = input("Enter email: ")
password = input("Enter password: ")

# Attempt to create or log in the user
try:
    # Attempt to create the user with email and password
    user = auth.create_user_with_email_and_password(email, password)
    print("User created successfully:", user)

    # After user creation, log them in automatically
    user = auth.sign_in_with_email_and_password(email, password)
    print(f"Logged in as {user['email']}")

except requests.exceptions.HTTPError as e:
    # Handle HTTP errors (e.g., weak password or email already in use)
    error_message = e.response.json().get('error', {}).get('message', '')
    if "EMAIL_EXISTS" in error_message:
        print("This email is already registered. Try logging in instead.")
    else:
        print(f"Error creating or logging in user: {error_message}")

except Exception as e:
    # Handle any other errors
    print(f"An error occurred: {e}")

# Function to add user data to Firebase
def add_user_to_db(user_id, name, role, expertise):
    user_data = {
        "name": name,
        "role": role,
        "expertise": expertise,
    }
    
    try:
        # Adding user data to the database
        db.child("users").child(user_id).set(user_data)
        print(f"User data for {name} added to the database.")
    except Exception as e:
        print(f"Error adding user data to database: {e}")

# Input for additional user data (Name, Role, and Expertise)
name = input("Enter your name: ")
role = input("Enter your role (mentor/peer): ")
expertise = input("Enter your expertise: ")

# Add the user data to the database
add_user_to_db(user['localId'], name, role, expertise)

# Function to add a meeting to the database
def add_meeting(mentor_id, mentee_id, time, status="pending"):
    try:
        # Validating the meeting time to ensure it is within allowed working hours (7:00 to 17:00, Monday to Friday)
        allowed_start_time = 7  # 07:00 AM
        allowed_end_time = 17  # 05:00 PM

        # Convert the input time into a datetime object
        meeting_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

        if meeting_time.hour < allowed_start_time or meeting_time.hour >= allowed_end_time:
            raise ValueError("Meeting time must be between 07:00 AM and 05:00 PM.")

        if meeting_time.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            raise ValueError("Meetings must be scheduled during weekdays (Monday to Friday).")
        
        # Push meeting details to Firebase
        meeting_ref = db.child("meetings").push({
            "mentor_id": mentor_id,
            "mentee_id": mentee_id,
            "time": time,
            "status": status
        })
        print(f"Meeting scheduled with mentor {mentor_id} for mentee {mentee_id} at {time}.")
    
    except ValueError as e:
        print(f"Error with meeting time: {e}")
    
    except Exception as e:
        print(f"Error scheduling meeting: {e}")

# Example: Add a meeting (Make sure the time format is correct)
mentor_id = input("Enter mentor's ID: ")  # Prompt for mentor's ID dynamically
meeting_time = input("Enter the meeting time (YYYY-MM-DD HH:MM:SS): ")
add_meeting(mentor_id, user['localId'], meeting_time)


