import smtplib


class MailSystem(object):
    login = "jobs.offer.scraper@gmail.com"
    password = "scraping.is.fun"
    receiver_email = "gara13@interia.pl"

    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    def send_mail_with_new_offers_num(self, message: str):
        self.smtp.ehlo()
        self.smtp.login(self.login, self.password)
        self.smtp.sendmail(self.login, self.receiver_email, message)
        self.smtp.close()

