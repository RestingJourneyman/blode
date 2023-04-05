import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyB99Pk1VQR0DZC3oxfrk-hOTjj5047Zzqc",
    "authDomain": "blode-9b777.firebaseapp.com",
    "projectId": "blode-9b777",
    "storageBucket": "blode-9b777.appspot.com",
    "messagingSenderId": "507827560184",
    "appId": "1:507827560184:web:642965ef77d3e52ec2e50d",
    "measurementId": "G-DHYRPJT5GQ",
    'databaseURL': "https://blode-9b777-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()