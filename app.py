from flask import Flask, render_template, request, session, g, url_for, flash, send_file
from flask import redirect
from modules.dashboard_data import get_data
from modules.data_process import data_processing
from modules.templates_data import cost_centers
from modules.authorize import request_to_authorize, authorization_process
from modules.employee_view import employee_view_data
from modules.download import prepare_download
from modules.notification import email_test
from share.db_init import db
import models.tables as mdls
import os
from flask_admin import Admin
from flask_mail import Mail
from templates.admin import admin_custom_views as adview  # Admin custom Views
from werkzeug.utils import secure_filename
from io import BytesIO

# DATABASE config
DATABASE_USER = 'root'
DATANBASE_PASSWORD = ''  # if not password leave it as:  ''
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'proverde'
DATABASE_PORT = '3307'


db_connection = 'mysql+pymysql://%s:%s@%s:%s/%s' % (DATABASE_USER, DATANBASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)  # NQAO configuration is as follows--> notchange+this://user:pass@host:(port if not 3306)/databasename
app = Flask(__name__) # webapp initialization
app.secret_key = os.urandom(24) # browser cookie setup
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'doc', 'docx']) # Not important for the time being

db.init_app(app)
admin = Admin(app)


#--- Mail config


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_PORT=587,
    MAIL_USERNAME='edward.dollars01@gmail.com',
    MAIL_PASSWORD='Sirallens24'
)

mail = Mail(app)


# -------------------------------login
@app.route('/')
def root_webapage():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' not in session:
        if request.method == 'POST':

            form_user = request.form.get('user')
            user = mdls.employee.query.filter_by(user=form_user).first()
            if user is not None:
                session['user'] = user.user
                session['name'] = user.name
                session['employee_id'] = user.id
                if user.department_assigned is not None:
                    session['department_assigned'] = user.department_assigned
                is_manager = mdls.manager.query.filter_by(manager_id=user.id).first()  # check if is Manager
                if is_manager is not None:
                    print("Manager")
                    print(is_manager.manager_id)
                    print(user.id)
                    session['manager'] = True
                    
                else:
                    print("Not manager")
                    session['manager'] = False
                    # email_test(mail)
                return redirect(url_for('dashboard'))

            else:
                flash('Invalid user. Use a valid user account', category='message') # NOQA
                return render_template('login.html')

        else:
            return render_template('login.html')
    else:
        return redirect(url_for('dashboard'))

# -------------------------------Submission Process


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'user' in session:
        if request.method == 'POST':


            notificate_to =  data_processing(request, db, g)
    
            return render_template('success.html', user=g.user)
        else:
            centers_dict = cost_centers()
            return render_template('submit.html', department=g.department, user=g.user, centers_dict=centers_dict)  # NOQA  To Ignore line lenght warning

    return redirect(url_for('login'))


# ------------------------------- user in session verification
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
        g.name = session['name']
        g.id = session['employee_id']
        if 'department_assigned' in session:
            g.department = session['department_assigned']
        if session['manager'] is True:
            g.is_manager = True
            
        else:
            g.is_manager = False
            print("g.user is not manager")
    

# ---------------------------------Dashboard-----------
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        data_list = get_data(db, g)
        print(data_list)
        if g.is_manager is True:
            return render_template('manager_dashboard.html', data_list=data_list, user=g.user)
        return render_template('dashboard.html', data_list=data_list, user=g.user)
    return redirect(url_for('login'))

# ------------------------------------------------------Authorize
@app.route('/authorize', methods=['GET', 'POST'])
def Authorize():
    if 'user' in session:
        
        folio = request.args.get('folio')
        data = request_to_authorize(db, g, folio)
        authorized = data['request_info']['needs_authorization']
        return render_template('authorization_view.html', data=data, user=g.user, authorized=authorized)
    return redirect(url_for('login'))


@app.route('/authorization_response', methods=['GET', 'POST'])
def authorization_response():
    if 'user' in session:
        if request.method == 'POST':
            print('authorization_response URL')
            authorize_bool_reponse = bool(int(request.form.get('authorize')))
            print(request.form.get('authorize'))
            print(authorize_bool_reponse)
            folio = request.args.get('folio')
            
            department = request.args.get('department')
            authorization_process(db, authorize_bool_reponse, folio, department, g)
            return render_template('success_manager.html', user=g.user)
        

# ------------------------------------- Request VIew -------------
@app.route('/view', methods=['GET'])
def Request_View():
    if 'user' in session:
        folio = request.args.get('folio')
        data_list = employee_view_data(db, folio)
        return render_template('request_view.html', user=g.user, data=data_list )
    return redirect(url_for('login'))


# --------------------------------------Send Downloadable file ---- 

@app.route('/download-file', methods=['GET'])
def download_file():
    folio = request.args.get('folio')
    download = prepare_download(db, folio)
    return send_file(BytesIO(download['data']), attachment_filename=download['filename'], as_attachment=True)

# ------------------------------------- Drop Session Log Out -------------
@app.route('/dropssession', methods=['GET'])
def dropsseion():

    if 'user' not in session:
        return redirect(url_for('login'))

    session.pop('user', None)
    return redirect(url_for('login'))

# ------------------------------------- Email Notification Processs -----------
@app.route('/notification', methods=['GET'])
def notification():
    if 'user' in session:
        pass
    return redirect(url_for('login')) 


# Custom Admin Views
admin.add_views(adview.EmployeeView(mdls.employee, db.session))
admin.add_views(adview.DepartmentView(mdls.department, db.session))
admin.add_views(adview.Department_ManagerView(mdls.manager, db.session))
admin.add_views(adview.RequestView(mdls.request, db.session))
admin.add_views(adview.ItemsView(mdls.items, db.session))
admin.add_views(adview.AuthorizationView(mdls.authorization, db.session))


# -------------------------------App Execution (For developement only, production execution is in a separated file) 

if __name__ == '__main__':
    app.run(debug=True)
