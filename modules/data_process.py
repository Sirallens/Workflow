import models.tables as mdls

# Just Plain text and numbers for the momment


def data_processing(object, db, g):

    item_info = {  # Blueprint for
        'description': 'description',
        'unit_measure': 'unit_measure',
        'chemical': 'chemical',
        'unit_price': 'unit_price',
        'quantity': 'quantity'

    }

    # request_object()
    
    print(object.form)

    form_dict = object.form
    item_list = []  # a Dictionary list that stores the Items in the request
    items_in_list = 1  # Int of how many items in request
    item_fieldID = 0  # Description=0, unit of measure=1, Chemical=2, Unit price=3, Quantity=4
    item = {}  # Dictionary of the each Item information (fields)

    total = 0.0  # Total cost of Request  (Sum of all item's [Quantity * Unit_Price])

    print(form_dict)

    request_info = {
        'purchase_type': form_dict['purchase_type'],
        'account_number': form_dict['account_number'],
        'cost_center': form_dict['cost_center']
    }

    while 1:   # Being 'data' a key from the form_dict
        if 'description_'+str(items_in_list) in form_dict:    # searches from tag_x   starting x with id 0
            print('aqui estoy')
            item['description'] = form_dict['description_'+str(items_in_list)]
            item['chemical'] = bool(form_dict['chemical_'+str(items_in_list)])
            item['unit_measure'] = form_dict['unit_measure_'+str(items_in_list)]
            item['unit_price'] = form_dict['unit_price_'+str(items_in_list)]
            item['quantity'] = form_dict['quantity_'+str(items_in_list)]
            item['item_total'] = float(item['unit_price']) * float(item['quantity'])

            total = total + item['item_total']

            if 'item_number_'+str(items_in_list) in form_dict:
                item['item_number'] = form_dict['item_number_'+str(items_in_list)]

            item_list.append(item)
            item = {}
            items_in_list += 1

        else:
            break

    new_request = mdls.request(
                               employee_id=g.id,
                               purchase_type=request_info['purchase_type'],
                               cost_center=request_info['cost_center'],
                               account_number=request_info['account_number'],
                               department_name=g.department,
                               comments=form_dict['comments'],
                               total=total
                               )

    if 'input_file' in object.files:
            file = object.files['input_file']
            print('guardar achivo')
            print(file.filename)
            if file.filename != '':
                new_request.file = file.read()
                new_request.filename = file.filename



    try:

        

        db.session.add(new_request)

        db.session.flush()
        print(new_request.folio)

        request_authorization = mdls.authorization(request_folio=new_request.folio)
        item_debug = 0

        print(item_list)

        for item in item_list:

            # totalprice = str(float(item['unit_price']) * float(item['quantity'])) - So far No needed
            item_debug += 1
            item_record = mdls.items(r_folio=new_request.folio,
                                     description=item['description'],
                                     chemical=item['chemical'],
                                     unit_measure=item['unit_measure'],
                                     unit_price=item['unit_price'],
                                     quantity=item['quantity'],
                                     item_total=item['item_total']
                                     )
            
            db.session.add(item_record)
            print(item_debug)
           
        db.session.add(request_authorization)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(e)

    return new_request.folio
