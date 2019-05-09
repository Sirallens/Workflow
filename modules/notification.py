import models.tables as mdls
from flask_mail import Message

def email_notification(db, folio):
    authorization_query = mdls.authorization.query.filter_by(request_folio=folio).first()

    if authorization_query.authorized == True:
        pass

    else:
        if authorization_query.authorization1 == None:
            pass

        if authorization_query.authorization1 == None:
            pass


def email_test(object):
    msg = Message("Prueba")
    msg.sender = 'edward.dollars01@gmail.com'
    msg.recipients = ['elchicogenio4@gmail.com']
    msg.body = 'Email Generado por Servidor'
    object.send(msg)
