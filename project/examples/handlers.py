from members.handlers import BaseApplicationHandler, BaseMemberHandler
from django.core.mail import EmailMessage
import logging
logger = logging.getLogger('example.handlers')



class ExampleBaseHandler(BaseMemberHandler):
    def on_saving(self, instance):
        msg = "on_saving called for %s %s" % (type(instance) , instance)
        logger.info(msg)
        print(msg)

    def on_saved(self, instance):
        msg = "on_saved called for %s %s" % (type(instance) , instance)
        logger.info(msg)
        print(msg)


class MemberHandler(ExampleBaseHandler):
    pass


class ApplicationHandler(ExampleBaseHandler):
    def on_approving(self, application, member):
        msg = "on_approving called for %s" % application
        logger.info(msg)
        print(msg)

    def on_approved(self, application, member):
        msg = "on_approved called for %s" % application
        logger.info(msg)
        print(msg)
        mail = EmailMessage()
        mail.to = [ member.email, ]
        mail.body = """Your membership has been approved, your member id is #%d""" % member.member_id
        mail.send()
