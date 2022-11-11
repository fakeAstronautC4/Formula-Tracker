from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
import os

db = SQLAlchemy()

def connect_to_db(flask_app, echo=False):
    # Setting up the function to connect the database to the app 
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://alons:hqO1451**Ken@localhost:5432/formula-tracker"
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")
##########################################################################################
class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String, nullable=False) #------------------------


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(40), unique=True, nullable = False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return (self.user_id)

    def __init__ (self, email, password):
        self.email = email
        self.password = password
    def __repr__(self):
        return f'User email - {self.email}'


class Formula(db.Model):
    __tablename__ = 'formulas'


    formula_id = db.Column(db.Integer, primary_key =True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    formula_code = db.Column(db.String, nullable = False, unique=True)
    name = db.Column(db.String(250), nullable = False, unique=True)
    description = db.Column(db.Text, nullable = False)
    customer = db.Column(db.String, nullable = True)
    init_visc = db.Column(db.Integer, nullable = True)
    init_pH = db.Column(db.Float, nullable = True)
    init_sg = db.Column(db.Float, nullable = True)


    user = db.relationship('User', backref='formulas')

    def __init__ (self, user_id, formula_code, name, description, customer="TBD", init_visc=0, init_pH=0, init_sg=0):
        self.user_id = user_id
        self.formula_code = formula_code
        self.name = name
        self.description = description
        self.customer = customer
        self.init_visc = init_visc
        self.init_pH = init_pH
        self.init_sg = init_sg

    def __repr__(self):
        return f'Formula_ID - {self.formula_id}\nUser_ID - {self.user_id}\nFormula Code - {self.formula_code}\nName - {self.name}\nDescription - {self.description}\nCustomer - {self.customer}\nInitial Viscosity - {self.init_visc}\nInitial pH - {self.init_pH}\nSpecific Gravity - {self.init_sg}'


class Material(db.Model):
    __tablename__ = 'materials'


    rm_id = db.Column(db.Integer, primary_key =True, autoincrement =True)
    rm_code = db.Column(db.String, nullable = False, unique = True)
    inci = db.Column(db.String, nullable = False, unique=True)
    vendor = db.Column(db.String, nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text, nullable = False)

    def __init__(self, rm_code, inci, vendor, price, description):
        self.rm_code = rm_code
        self.inci = inci
        self.vendor = vendor
        self.price = price
        self.description = description

    def __repr__(self):
        return(f"Material Code - {self.rm_code}\nInci - {self.inci}\nVendor - {self.vendor}\nPrice - {self.price}\nDescription - {self.description}")



##########################################################################################
if __name__ == '__main__':
    from server import app
    connect_to_db(app)