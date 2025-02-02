import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("../creds.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pantry-pal-1a39b-default-rtdb.firebaseio.com/'
})

ref = db.reference('User1/Product A')
data = {"Count": 10}
ref.update(data)

ref = db.reference('User2/Product A')
data = {"Count": 5}
ref.update(data)

print("Data uploaded successfully!")
