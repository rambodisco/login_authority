from models import *
from flask import render_template,request

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        formdata=request.form
        x = formdata.get('name')
        print(x)
        y = formdata.get('password')
        print(y)
        try:
            user=User.query.filter_by(name=x).first()
            message = 'invalid username and password'
            if user.name==x:
                if user.password == y:
                    return render_template('index.html')
                return render_template('login.html', message=message)
        except:
            message = 'invalid username and password'
            return render_template('login.html', message=message)
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        formdata=request.form
        errors=[]
        if not formdata.get('username'):
            errors.append('User name cannot be empty')
        if not formdata.get('email'):
            errors.append('email cannot be empty')
        if not formdata.get('password'):
            errors.append('password cannot be empty')

        if errors:
            return render_template('register.html',errors=errors)

        try:
            user= User( name = formdata.get('username'),
                        email = formdata.get('email'),password = formdata.get('password'))
            db.session.add(user)
            db.session.commit()
        except:
            return render_template('register.html', message='already user present please try different name...')

        return render_template('register.html',message= 'user add successfully')

    return render_template('register.html')


@app.route('/index')
def index_page():
    return render_template('index.html')

@app.route('/add-emp',methods=['GET'])
@app.route('/emp-save',methods=['GET','POST'])
def add_employee():
    if request.method=='POST':
        formdata = request.form
        print(formdata)

        errors=[]

        if not formdata.get('ename'):
            errors.append('Employee name cannot be empty...')
        if not formdata.get('email'):
            errors.append('Employee name cannot be empty...')
        if not formdata.get('esal'):
            errors.append('Employee salary cannot be empty...')
        else:
            try:
                salary = float(formdata.get('esal'))
                if salary<=0:
                    errors.append('Invalid salary...')

            except:
                errors.append('Invalid salary...')

        if errors:
            return render_template('addemployee.html', emessage=errors)

        employee=Employee(id=formdata.get('eid'),name=formdata.get('ename'),email=formdata.get('email'),
                 role=formdata.get('erole'),dept=formdata.get('edept'),salary=salary)
        db.session.add(employee)
        db.session.commit()
        return render_template('addemployee.html',message='Employee added successfully...')

    return render_template('addemployee.html')

@app.route('/emp-delete/<int:eid>')
def delete_employee(eid):
    employee=Employee.query.filter_by(id=eid).first()
    db.session.delete(employee)
    db.session.commit()

    return render_template('listemployee.html',elist=Employee.query.all())


def search_employee():
    pass


@app.route('/emp-edit/<int:eid>')
@app.route('/emp-edit/', methods=['POST'])
def update_employee(eid=None):
    if request.method == 'GET':
        employee=Employee.query.filter_by(id=eid).first()
        return render_template('updateemployee.html', record=employee)
    else:
        formdata = request.form
        eid = formdata.get('eid')
        employee=Employee.query.filter_by(id=eid).first()
        employee.name = formdata.get('ename')
        employee.role = formdata.get('erole')
        employee.salary = formdata.get('esal')
        employee.dept= formdata.get('edept')
        employee.email = formdata.get('email')

        db.session.commit()

        return render_template('listemployee.html', elist=Employee.query.all())



@app.route('/emp-list')
def list_employee():
    return render_template('listemployee.html', elist=Employee.query.all())


SORT_SAL = True
SORT_DEPT = True
@app.route('/sort/<by>')
def sort_employee(by):
    global SORT_SAL
    global  SORT_DEPT
    employees = Employee.query.all()
    employees = list(employees)
    if by == 'sal':
        employees.sort(key=lambda item : item.salary,reverse=SORT_SAL)
        SORT_SAL = False if SORT_SAL else True
    elif by=='dept':
        employees.sort(key=lambda item: item.dept, reverse=SORT_DEPT)
        SORT_DEPT = False if SORT_DEPT else True
    else:
        employees.sort(key=lambda item: item.id)

    return render_template('listemployee.html', elist=employees)


# SORT_SAL=True
# SORT_DEPT=True
# @app.route('/sort/<by>')
# def sort_employee(by):
#     global SORT_SAL
#     global SORT_DEPT
#     employees= Employee.query.all()
#     employees=list(employees)
#     if by =='sal':
#         employees.sort(key=lambda item:item.salary,reverse=SORT_SAL)
#         SORT_SAL = False if SORT_SAL else True
#     if by=='dept':
#         employees.sort(key=lambda item:item.dept,reverse=SORT_DEPT)
#         SORT_DEPT = False if SORT_DEPT else True
#     else:
#         employees.sort(key=lambda item:item.id)
#
#     return render_template('listemployee.html', elist=employees)

@app.route('/emp-sal-range',methods=['POST'])
def emp_salary_range():
    formdata = request.form
    start_range = float(formdata.get('fsal'))
    end_range = float(formdata.get('esal'))
    message = " "
    if start_range<=0 or end_range<=0:
        message='Invalid salary range'
    elif start_range<end_range:
        employees=Employee.query.filter(Employee.salary>=start_range,Employee.salary<=end_range).all()
        if employees:
            return render_template('listemployee.html', emps=employees,elist=Employee.query.all())
        message='No record with given range'
    return render_template('listemployee.html', message = message,elist=Employee.query.all())