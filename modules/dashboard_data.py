import models.tables as mdls


def authorization_status(object):
    if object is None:
        return "Pending..."
    elif object is True:
        return 'Approved'
    else:
        return 'Declined'


def get_department_requests(object, data, department_managed, auth_query=list()):

    '''if department_managed == 'Planta':
        request_folio_by_authorization = mdls.authorization.query.filter_by(authorization1=True).all()
    elif department_managed == 'Finanzas':
        request_folio_by_authorization = mdls.authorization.query.filter_by(authorization2=True).all()
    else:
        pass  # Should not get here

    print(department_managed)
'''
    request_container = mdls.request.query.all()


    if request_container is not None:
        for single_request in request_container:
            request = {}
            authorization = mdls.authorization.query.filter_by(request_folio=single_request.folio).first()

            if department_managed == 'Planta' and authorization.authorization1 is True: 
                
                request['folio'] = single_request.folio
                request['employee_id'] = single_request.employee_id
                request['submit_date'] = single_request.submit_date
                request['total'] = single_request.total
                request['authorization'] = authorization_status(authorization.authorized)
                request['department'] = single_request.department_name
                if authorization.authorization2 is None:
                    request['needs_authorization'] = True
                data.append(request)

            elif department_managed == 'Finanzas' and authorization.authorization2 is True:
                print("finanzas dashboard")
                
                request['folio'] = single_request.folio
                request['employee_id'] = single_request.employee_id
                request['submit_date'] = single_request.submit_date
                request['total'] = single_request.total
                request['authorization'] = authorization_status(authorization.authorized)
                request['department'] = single_request.department_name
                if authorization.authorization3 is None:
                    request['needs_authorization'] = True
                data.append(request)

            elif department_managed == single_request.department_name: 
                
                request['folio'] = single_request.folio
                request['employee_id'] = single_request.employee_id
                request['submit_date'] = single_request.submit_date
                request['total'] = single_request.total
                request['authorization'] = authorization_status(authorization.authorized)
                request['department'] = single_request.department_name
                if authorization.authorization1 is None:
                    request['needs_authorization'] = True
                data.append(request)

            else:
                pass  # request not ready for either Plant Manager or Finance Manager

    return data


def get_data(object, g):

    if g.is_manager is True:
        departments_supervising = mdls.manager.query.filter_by(manager_id=g.id).all()
        plant_manager = mdls.manager.query.filter_by(manager_id=g.id, department_name='Planta').first()
        finance_manager = mdls.manager.query.filter_by(manager_id=g.id, department_name='Finanzas').first()

        data = []

        if plant_manager is not None:
            request_folio_by_authorization = mdls.authorization.query.filter_by(authorization1=True).all()
            data = get_department_requests(object, data, 'Planta')

        elif finance_manager is not None:
            request_folio_by_authorization = mdls.authorization.query.filter_by(authorization2=True).all()
            data = get_department_requests(object, data, 'Finanzas')

        elif departments_supervising is not None:
            for department in departments_supervising:
                data = get_department_requests(object, data, department.department_name)

        else:
            pass  # No requests

    else:
        request_container = mdls.request.query.filter_by(employee_id=g.id).all()
        request = {}
        data = []

        if request_container is not None:
            for single_request in request_container:
                authorization = mdls.authorization.query.filter_by(request_folio=single_request.folio).first()
                
                request['folio'] = single_request.folio
                request['employee_id'] = single_request.employee_id
                request['submit_date'] = single_request.submit_date
                request['total'] = single_request.total
                request['authorization'] = authorization_status(authorization.authorized)
                request['department'] = single_request.department_name

                data.append(request)
                request = {}

        else:
            pass  # No requests

    return sorted(data, key=lambda i: i['authorization'], reverse=True) 


