import models.tables as mdls
from modules.dashboard_data import authorization_status


def employee_view_data(object, folio):
    request_query = mdls.request.query.filter_by(folio=folio).first()
    authorization_query = mdls.authorization.query.filter_by(request_folio=folio).first()
    items_query = mdls.items.query.filter_by(r_folio=folio)
    employee = mdls.employee.query.filter_by(id=request_query.employee_id).first()
    data = {}
    request_information = {}
    item_list = []

    request_information['folio'] = request_query.folio
    request_information['purchase_type'] = request_query.purchase_type
    request_information['employee_id'] = request_query.employee_id
    request_information['name'] = employee.name
    request_information['purchase_order'] = request_query.purchase_order
    request_information['cost_center'] = request_query.cost_center
    request_information['account_number'] = request_query.account_number
    request_information['department_name'] = request_query.department_name
    request_information['total'] = request_query.total
    request_information['comments'] = request_query.comments
    
    if authorization_query.authorization1 is not None:  # Department Manager authozation details
        request_information['authorizer1'] = mdls.employee.query.filter_by(id=authorization_query.authorization1_by).first().name # NOQA
        request_information['authorization1'] = authorization_status(authorization_query.authorization1)  # NOQA
        request_information['date1'] = authorization_query.authorization1_date

        if authorization_query.authorization2 is not None:  # Plant Manager authorization details
            request_information['authorizer2'] = mdls.employee.query.filter_by(id=authorization_query.authorization2_by).first().name  # NOQA
            request_information['authorization2'] =  authorization_status(authorization_query.authorization2)  # NOQA
            request_information['date2'] = authorization_query.authorization2_date

            if authorization_query.authorization3 is not None: # Finance manager authorization details
                request_information['authorizer3'] = mdls.employee.query.filter_by(id=authorization_query.authorization3_by).first().name # NOQA
                request_information['authorization3'] = authorization_status(authorization_query.authorization3) # NOQA
                request_information['date3'] = authorization_query.authorization3_date
            else:
                request_information['authorizer3'] = 'TBD'  # NOQA

        else:
            request_information['authorizer2'] = 'TBD'  # NOQA
    else:
        request_information['authorizer1'] = 'TBD'  # NOQA
        



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
