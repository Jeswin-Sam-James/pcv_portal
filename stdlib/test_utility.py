import logging
import sender




def test_exception_mail_send(portal_name,client_name,ex):
    """This Function is used to send Exception  Mails"""
    try:
        mail = sender.Mail('smtp.gmail.com', 'murcorpcv@gmail.com' , 'ekmw pldz tdhw zkkp', 465, use_ssl=True,fromaddr='murcorpcv@gmail.com')
        logging.info('Connected to email')
        err_message = """This is an automatic notification:
Exception in {}'s {} account.

Exception in {}
""".format(client_name,portal_name,ex)
        logging.info(err_message)

        mail.send_message(subject=f'{portal_name} Exception!', to='murcorpcv@gmail.com', body=err_message)
        logging.info('Exception Mail sent')
    except Exception as ec:
        logging.info(ec)