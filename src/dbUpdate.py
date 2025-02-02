import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("creds.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pantry-pal-1a39b-default-rtdb.firebaseio.com/'
})

def updateDatabase(updates, ID, name, date, insert):
    if insert:
        if ID not in updates:
            updates[ID] = {"name": name}
            updates[ID]["dates"] = {"date1": date}

        else:
            l = len(updates[ID]["dates"])
            updates[ID]["dates"]["date" + str(l + 1)] = date

    else:
        if ID in updates:
            l = len(updates[ID]["dates"])
            
            if l == 1:
                updates[ID] = None

            else:
                for i in range(l - 1):
                    updates[ID]["dates"]["date" + str(i + 1)] = updates[ID]["dates"]["date" + str(i + 2)]

                updates[ID]["dates"]["date" + str(l)] = None


    ref.update(updates)
    updates = ref.get()


