import models.tables as mdls


def request_to_authorize(db, g, folio):
    data = {}
    request = mdls.request.query.filter_by(folio=folio).first()
    items_query = mdls.items.query.filter_by(r_folio=folio).all()
    employee = mdls.employee.query.filter_by(id=request.employee_id).first()
    request_information = {}
    item_list = []
    request_information['folio'] = request.folio
    request_information['purchase_type'] = request.purchase_type
    request_information['employee_id'] = request.employee_id
    request_information['name'] = employee.name
    request_information['purchase_order'] = request.purchase_order
    request_information['cost_center'] = request.cost_center
    request_information['account_number'] = request.account_number
    request_information['department_name'] = request.department_name
    request_information['total'] = request.total
    request_information['comments'] = request.comments
    # send file to be implemented
    
    manager_of = mdls.manager.query.filter_by(manager_id=g.id).first()
    authorization_query = mdls.authorization.query.filter_by(request_folio=folio).first()
    
    print(manager_of.department_name)

    if manager_of.department_name != 'Planta' and manager_of.department_name != 'Finanzas':
        print('Estoy en auth1')
        if authorization_query.authorization1 is None:
            request_information['needs_authorization'] = True
            request_information['auth_from'] = manager_of.department_name

        else:
            request_information['needs_authorization'] = False
            request_information['auth_response'] = authorization_query.authorization1

    elif manager_of.department_name == 'Planta':
        print('Estoy en auth2')
        if authorization_query.authorization2 is None:
            request_information['needs_authorization'] = True
            request_information['auth_from'] = 'Planta'
        else:
            request_information['needs_authorization'] = False
            request_information['auth_response'] = authorization_query.authorization2
            

    elif manager_of.department_name == 'Finanzas':
        print('Estoy en auth3')
        if authorization_query.authorization3 is None:
            print(authorization_query.authorization3)
            request_information['needs_authorization'] = True
            request_information['auth_from'] = 'Finanzas'
        else:
            print(authorization_query.authorization3)
            request_information['needs_authorization'] = False
            request_information['auth_response'] = authorization_query.authorization3
            

    else:
        pass  # Should not get here 

    
    print(request.filename)
    print(request_information['needs_authorization'])
    
    if request.filename is not None:
        request_information['attachment'] = True

    data['request_info'] = request_information

    for item in items_query:
        item_info = {}
        item_info['description'] = item.description
        item_info['chemical'] = item.chemical
        item_info['unit_measure'] = item.unit_measure
        item_info['unit_price'] = item.unit_price
        item_info['quantity'] = item.quantity
        item_info['item_total'] = item.item_total
        item_info['item_number'] = item.item_number
        item_list.append(item_info)

    data['item_list'] = item_list

    return data


def authorization_process(object, response, folio, department, g):
    authorization_query = mdls.authorization.query.filter_by(request_folio=folio).first()
    print(folio)
    print(department)
    print('authorize_process')
    print(authorization_query)
    try:
        if authorization_query.authorization3 is None and department == 'Finanzas':
            authorization_query.authorization3 = response
            authorization_query.authorization3_date = mdls.td.datetime.now()
            authorization_query.authorization3_by = g.id
            authorization_query.authorized = response
            

        elif authorization_query.authorization2 is None and department == 'Planta':
            authorization_query.authorization2 = response
            authorization_query.authorization2_date = mdls.td.datetime.now()
            authorization_query.authorization2_by = g.id
            if response is False:
                authorization_query.authorized = response

            

        elif authorization_query.authorization1 is None and department != 'Planta' and department != 'Finanzas':
            authorization_query.authorization1 = response
            authorization_query.authorization1_date = mdls.td.datetime.now()
            authorization_query.authorization1_by = g.id
            if response is False:
                authorization_query.authorized = response
            
        else:
            pass  # should not get here

        print(authorization_query.authorization2)
        object.session.commit()

    except Exception as err:
        print(err)
        object.session.rollback()
