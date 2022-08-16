# from flask import Flask
# from flask_mail import Mail, Message
# import os
#
# app = Flask(__name__)
#
# mail_settings = {
#     "MAIL_SERVER": 'smtp.gmail.com',
#     "MAIL_PORT": 465,
#     "MAIL_USE_TLS": False,
#     "MAIL_USE_SSL": True,
#     "MAIL_USERNAME": os.environ['takeitapp0@gmail.com'],
#     "MAIL_PASSWORD": os.environ['eR6uI6hS0xG4qI3y']
# }
#
# app.config.update(mail_settings)
# mail = Mail(app)
# @app.route('/send-mail/')
#
#
# def send_mail():
#     msg = mail.send_message(
#         'Send Mail tutorial!',
#         sender='takeitapp0@gmail.com',
#         recipients=['guyshmuel93@gmail.com'],
#         body="Congratulations you've succeeded!"
#     )
#     return 'Mail sent'