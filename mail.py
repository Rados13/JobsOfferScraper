import smtplib
import json
import os


class MailSystem(object):

    def __init__(self):
        """
        local version
        with open("creditentials.json") as json_file:
            data = json.load(json_file)
            self.login = data["login"]
            self.password = data["password"]
            self.receiver_email = data["receiver_email"]
        """
        self.login = os.environ.get("login")
        self.password = os.environ.get("password")
        self.receiver_email = os.environ.get("receiver_email")

    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    def send_mail_with_new_offers_num(self, message: str):
        self.smtp.ehlo()
        self.smtp.login(self.login, self.password)
        self.smtp.sendmail(self.login, self.receiver_email, message)
        self.smtp.close()
