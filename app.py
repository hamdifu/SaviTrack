import pyrebase

config = {
    'apiKey': "AIzaSyCmEAjhCukCW2R_kidV8-c9Ln9_PdSAZII",
    'authDomain': "pricetracker-5e30c.firebaseapp.com",
    'projectId': "pricetracker-5e30c",
    'databaseURL': 'https://pricetracker-5e30c-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': "pricetracker-5e30c.appspot.com",
    'messagingSenderId': "210337986734",
    'appId': "1:210337986734:web:e21ec17fa4601cd7a9153f",
    'measurementId': "G-489TCP34PH",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()