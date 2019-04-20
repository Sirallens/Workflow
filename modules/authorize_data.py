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
    request_information['name'] = employee.id
    request_information['purchase_order'] = request.purchase_order
    request_information['cost_center'] = request.cost_center
    request_information['account_number'] = request.account_number
    request_information['department_name'] = request.department_name
    request_information['total'] = request.total
    request_information['comments'] = request.comments
    # send file to be implemented
    
    manager_of = mdls.manager.query.filter_by(manager_id=g.id).first()
    authorization_query = mdls.authorization.query.filter_by(request_folio=folio).first()
    
    if manager_of.department_name != 'Planta' and manager_of.department_name != 'Planta':
        if authorization_query.authorization1 is None:
            request_information['needs_authorization'] = True

        else:
            request['needs_authorization'] = False

    elif manager_of.department_name == 'Planta':
        if authorization_query.authorization2 is None:
            request_information['needs_authorization'] = True
        else:
            request_information['needs_authorization'] = False

    elif manager_of.department_name != 'Finanzas':
        if authorization_query.authorization3 is None:
            request_information['needs_authorization'] = True
        else:
            request_information['needs_authorization'] = False

    else:
        pass  # Should not get here 

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
