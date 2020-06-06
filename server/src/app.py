import pyrebase
import random
from flask import *
import firebase_admin
from firebase_admin import credentials,firestore
import time




coln=['a','b','c','d','e','A','B','C','D','E','AB','AC','AD','AE','ab','ac','ad','ae']

cred= credentials.Certificate('firebase-sdk.json')

firebase_admin.initialize_app(cred)

db= firestore.client()


config={
    'apiKey': "AIzaSyBfJzyEYrHaC9gif8j1CCu3xiVz0xyKyAk",
    'authDomain': "form-storage123.firebaseapp.com",
    'databaseURL': "https://form-storage123.firebaseio.com",
    'projectId': "form-storage123",
    'storageBucket': "form-storage123.appspot.com",
    'messagingSenderId': "733283442227",
    'appId': "1:733283442227:web:2fbca028e09cb40c178d46",
    'measurementId': "G-0JPT3X5NYR"
}

firebase=pyrebase.initialize_app(config)
auth = firebase.auth()
firebase=pyrebase.initialize_app(config)

storage=firebase.storage()

app = Flask(__name__)
app.secret_key = b'_8#y2L"F4Q8z\n\xec]/'

@app.route('/home')
def home():
   return render_template('first.html')

@app.route('/')
def register():
   return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def Register():
   if request.method=='POST':
       name=request.form['name']
       mobile=request.form['mobile']
       email=request.form['email']
       type=request.form['type']
       num=request.form['num']
       picture=request.files['image']
       regid=f'STACK{random.choice(coln)}{name}_{random.randint(1000,9999)}'
       if type=='Self':
          num=1
       try:
           doc_ref= db.collection('user_data').document(regid)
           doc_ref.set({
               'name': name,
               'mobile': mobile,
               'email': email,
               'type': type,
               'num': num,
               'regid':regid
           })
           
           storage.child(f'images/{regid}.jpg').put(picture)
           y=storage.child(f'images/{regid}.jpg').get_url(None)
           return render_template('success.html',name=name,mobile=mobile,email=email,type=type,num=num,regid=regid,y=y)
       except Exception :
            print(Exception)
            return render_template('success.html')

@app.route('/adminlogin')
def adminlogin():
   return render_template('adminLogin.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminLogin():
   if request.method=='POST':
       email=request.form['email']
       password=request.form['password']
       try:
           login=auth.sign_in_with_email_and_password(email,password)
           return redirect(url_for('admindashboard'))
       except:
           flash('The Username or password dosent match the records')
           return redirect(url_for('adminlogin'))

@app.route('/admindashboard')
def admindashboard():
   return render_template('dashboard.html')

@app.route('/userlogin')
def userlogin():
   return render_template('userLogin.html')

@app.route('/userlogin', methods=['GET', 'POST'])
def userLogin():
   if request.method=='POST':
      name=request.form['name']
      regid=request.form['regid']
      # print(regid)
      try:
         user=db.collection(u'user_data').where('regid','==',f'{regid}').stream()
         for doc in user:
            # print(u'{} => {}'.format(doc.id, doc.to_dict()))
            x=doc.to_dict()
         # print(x['name'])
         y=storage.child(f'images/{regid}.jpg').get_url(None)
         return render_template('success.html',name=x['name'],mobile=x['mobile'],email=x['email'],type=x['type'],num=x['num'],regid=regid,y=y)
      except:
         flash('User was not found please check the given id')
         return redirect(url_for('userlogin'))


if __name__ == "__main__":
    app.run(debug=True)