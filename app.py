from asyncio import constants
from sre_constants import SUCCESS
from turtle import pen
from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.tatoo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)
sms = ''
class Inventars(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    inventar_name = db.Column(db.String(20), unique = False, nullable = False)
    inventar_coast = db.Column(db.String(20), unique = False, nullable = False)
    condition = db.Column(db.String,unique=False, nullable = False)

    def __repr__(self):
        return f"inventar_name : {self.inventar_name}, inventar_coast : {self.inventar_coast}, condition : {self.condition}"

@app.route('/',methods=['GET','POST'])
def hm():
    if request.method == 'GET':
      return render_template('add_items_and_see.html',active = 'active',success='false')
    if request.method == 'POST':
      name = request.values.get('inventarName')
      coast = request.values.get('inventarCoast')
      condition = request.values.get('inventarCondition')
      if(len(name) != 0 and len(coast) != 0 and len(condition) != 0):
         code = Inventars(inventar_name = name, inventar_coast = coast, condition = condition)
         db.session.add(code)
         db.session.commit()
         return redirect(url_for('inventars', success2 = 'true'))

@app.route('/inventars',methods = ['GET','POST'])
def inventars():
    if request.method == 'GET':
        information = Inventars.query.all()
        success1  = request.args.get('success1')
        success2 = request.args.get('success2')
        name = request.args.get('name')
        return render_template('inventars.html', active1 = 'active',list = information,success1 = success1,success2 = success2,name = name)
    if request.method == 'POST':
        key = list(request.values.keys())
        key= key[0]
        data = Inventars.query.get(key)
        db.session.delete(data)
        db.session.commit()
        information = Inventars.query.all()
        sms = 'item deleted from database'
        
        return render_template('inventars.html', active1 = 'active',list = information,success = 'true',sms = sms)

@app.route('/update:<id>',methods=['GET','POST'])
def update(id):
        data = Inventars.query.get(id)
        return render_template('update.html',active2 = 'active',data = data,id = id,success = 'false')

@app.route('/update',methods = ['POST'])
def update2():
     key = list(request.values.keys())
     print(key)
     key1 = 0
     for i in key:
         if i.isnumeric():
             key1 = i
             break
     new_name,new_coast,new_condition = request.values.get(key1),request.values.get('inventarCoast'),request.values.get('inventarCondition')
     updateOned = Inventars.query.get(key1)
     updateOned.inventar_name,updateOned.inventar_coast,updateOned.condition = new_name, new_coast, new_condition
     db.session.commit()
     print(updateOned.inventar_name)
     return  redirect(url_for('.inventars', success1 = 'true', name = updateOned.inventar_name))
if __name__ == "__main__":
    app.run(debug=True)