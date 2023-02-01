
from config import *

class User(db.Model):
    userid = db.Column('user_id',db.Integer(),primary_key=True)
    name = db.Column('user_name',db.String(50),unique=True)
    email = db.Column('user_email',db.String(50),unique=True)
    password= db.Column('user_dept',db.String(50))


class Employee(db.Model):
    id = db.Column('emp_id',db.Integer(),primary_key=True)
    name = db.Column('emp_name',db.String(50))
    email = db.Column('emp_email',db.String(50),unique=True)
    dept= db.Column('emp_dept',db.String(50))
    role = db.Column('emp_role',db.String(50))
    salary = db.Column('emp_salary',db.Float)



with app.app_context():
    db.create_all()
    print('Tables created...')

