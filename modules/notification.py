import models.tables as mdls
from flask_mail import Message
import win32com.client as win32

def email_notification_workflow(db, folio):
    authorization_query = mdls.authorization.query.filter_by(request_folio=folio).first()
    request_info = mdls.request.query.filter_by(folio=folio).first()

    if authorization_query.authorized is True:
        pass

    else:
        if authorization_query.authorization1 is None:
            manager = mdls.manger.query.filter_by(department=request_info.department)
            email_generator(manager, request_info)

        if authorization_query.authorization2 is None:
            manager = mdls.manager.query.filter_by(department='Planta').first()
            email_generator(manager, request_info)

        if authorization_query.authorization3 is None:
            manager = mdls.manager.query.filter_by(department='Finanzas').first()
            email_generator(manager, request_info)


def email_generator(manager, request):
    destination = manager + "@ascopower.com"

    message = """

        You have a new workflow.
        A new request with Folio(ID) %s from %s requires and action.


    """ % (str(request.folio), request.department)
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = destination
    mail.Subject = 'New workflow inbound'
    mail.Body = message
    # attachment = "file"  # To attach a file to the email (optional):
    # mail.Attachments.Add(attachment)

    mail.Send()


def email_test(object):
    msg = Message("Prueba")
    msg.sender = 'edward.dollars01@gmail.com'
    msg.recipients = ['elchicogenio4@gmail.com']
    msg.body = 'Email Generado por Servidor'
    object.send(msg)
