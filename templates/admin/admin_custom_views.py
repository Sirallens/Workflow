from flask_admin.contrib.sqla import ModelView


class EmployeeView(ModelView):
    column_display_pk = True
    column_hide_backref = False
    column_hide_ibackref = False
    form_columns = ['id', 'name', 'user', 'department_assigned']


class RequestView(ModelView):
    column_display_pk = True
    column_hide_backref = False
    form_columns = ['folio', 'employee_id', 'purchase_order', 'comments']
    can_create = False
    can_delete = False


class DepartmentView(ModelView):
    column_display_pk = True
    column_hide_backref = False
    form_columns = ['name']


class Department_ManagerView(ModelView):
    column_hide_backrefs = False
    column_display_pk = True
    form_columns = ['manager_id', 'department_name']


class AuthorizationView(ModelView):
    column_hide_backrefs = False


class ItemsView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False