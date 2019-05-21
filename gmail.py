import smtplib

gmail_user = 'edward.dollars@@gmail.com'  
gmail_password = 'Sirallens24'

try:  
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(gmail_user, gmail_password)
    message = "Message_you_need_to_send"
    s.sendmail(gmail_user, 'elchicogenio4@hotmail.com', message)
    s.quit()
    print('Email sent!')


except:
    print('Something went wrong...')
