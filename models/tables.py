from share.db_init import db
from sqlalchemy.dialects.mysql import MEDIUMBLOB
import datetime as td

'''
department_workers = db.Table('deparment_manager',
    db.Column('manager_id', db.Integer, db.ForeignKey("employee.id", onupdate='CASCADE'), nullable=True), # NOQA  To Ignore line lenght warning
    db.Column('department_name', db.String(50), db.ForeignKey('department.name', onupdate='CASCADE')) # NOQA
)'''


class employee(db.Model): 
    # fields here

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(50), nullable=False)
    # last_name = db.Column(db.String(50), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    department_assigned = db.Column(db.String(50), db.ForeignKey('department.name'), nullable=True)
    manages = db.relationship('manager', backref='manager', lazy='select')
    # requester = db.relationship('employee', backref='request')  relation employee --> Request


    def __repr__(self):
        return '<Employee %r with Id %r>' % (self.name, self.id)


class department(db.Model):
    # fields here
    name = db.Column(db.String(50), primary_key=True)
    worker = db.relationship('employee', backref='deparment_Assigned', lazy='select')
    manager = db.relationship('manager', backref='department', lazy='select', uselist=False)

    def __repr__(self):
        return '<Department %r>' % (self.name)


class manager(db.Model):
    department_name = db.Column(db.String(50), db.ForeignKey('department.name'), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    

'''

class department_manager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # NOQA - Irrelevant. but needed to suffice SQLAlchemy conventions
    manager_id = db.Column(db.Integer, db.ForeignKey("employee.id", onupdate='CASCADE'), nullable=True,) # NOQA  To Ignore line lenght warning
    department_name = db.Column(db.String(50), db.ForeignKey('department.name', onupdate='CASCADE')) # NOQA
'''


class items(db.Model):
    # fields here
    r_folio = db.Column(db.Integer, db.ForeignKey("request.folio", ondelete='CASCADE')) # NOQA - To Ignore line lenght warning
    folio = db.relationship('request', backref='items')
    description = db.Column(db.String(100), primary_key=True) # NOQA 
    chemical = db.Column(db.Boolean(), nullable=False)
    unit_measure = db.Column(db.String(3), nullable=False)
    unit_price = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_total = db.Column(db.Float(precision=2), nullable=False)
    item_number = db.Column(db.String(50), nullable=True)


class request(db.Model):
    # fields here
    folio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authorization_id = db.relationship('authorization', backref='authorization_folio')    # Not a Column, but relation for schema 
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False) # NOQA  To Ignore line lenght warning
    submit_date = db.Column(db.DateTime(), nullable=False, default=td.datetime.now()) # NOQA  To Ignore line lenght warning
    purchase_type = db.Column(db.String(20), nullable=False)
    purchase_order = db.Column(db.String(20), nullable=True)
    cost_center = db.Column(db.String(20), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    department_name = db.Column(db.String(50), db.ForeignKey('department.name'), nullable=False)
    total = db.Column(db.Float(precision=2), nullable=True)
    comments = db.Column(db.String(256), nullable=True)
    file = db.Column(MEDIUMBLOB(), nullable=True)
    filename = db.Column(db.String(50), nullable=True)


class authorization(db.Model):
    # fields here
    request_folio = db.Column(db.Integer, db.ForeignKey("request.folio"), primary_key=True) # NOQA  To Ignore line lenght warning
    authorized = db.Column(db.Boolean)
    authorization1 = db.Column(db.Boolean, nullable=True)
    authorization1_date = db.Column(db.DateTime, nullable=True)
    authorization1_by = db.Column(db.Integer, db.ForeignKey('manager.manager_id')) # Dpt Manager
    authorization2 = db.Column(db.Boolean, nullable=True)
    authorization2_date = db.Column(db.DateTime, nullable=True)
    authorization2_by = db.Column(db.Integer, db.ForeignKey('manager.manager_id')) # Plant manager 
    authorization3 = db.Column(db.Boolean, nullable=True)
    authorization3_date = db.Column(db.DateTime, nullable=True)
    authorization3_by = db.Column(db.Integer, db.ForeignKey('manager.manager_id')) # Finance Manager


# TODO Cost_center

'''class cost_center(db.Model):
    pass'''



