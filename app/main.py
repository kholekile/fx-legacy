from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import mail
import datetime
import webapp2
import jinja2
import os
import json
import urllib
import logging
import models
import re
import sms
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Home(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render())

class About(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/about.html')
        self.response.out.write(template.render())

class AutoTrading(webapp2.RequestHandler):
    def get(self):
        churches = models.Church.get_available_churches()
        template = jinja_environment.get_template('templates/auto-trading.html')
        self.response.out.write(template.render({'churches': churches}))

class ForexTraining(webapp2.RequestHandler):
    def get(self):
        slots = models.City.get_available_slots()
        churches = models.Church.get_available_churches()
        template = jinja_environment.get_template('templates/forex-training.html')
        self.response.out.write(template.render({'slots': slots,'churches': churches}))

class ForexSeminar(webapp2.RequestHandler):
    def get(self):
        churches = models.Church.get_available_churches()
        template = jinja_environment.get_template('templates/forex-seminar.html')
        self.response.out.write(template.render({'churches':churches}))

class ComparePackages(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/compare-packages.html')
        self.response.out.write(template.render())

class Services(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/services.html')
        self.response.out.write(template.render())

class TermsAndConditions(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/terms-and-conditions.html')
        self.response.out.write(template.render())

class RiskWarning(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/risk-warning.html')
        self.response.out.write(template.render())

class PrivacyPolicy(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/privacy-policy.html')
        self.response.out.write(template.render())

class ContactUs(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/contact.html')
        self.response.out.write(template.render())

class CreateTrainingMember(webapp2.RequestHandler):
    def post(self):
        slots = models.City.get_available_slots()
        churches = models.Church.get_available_churches()
        savedMember = False
        updatedSlot = False

        title = self.request.get("title")
        firstName = self.request.get("firstname")
        lastname = self.request.get("lastname")
        idnumber = self.request.get("idnumber")
        cellPhoneNumber = self.request.get("cellPhoneNumber")
        email = self.request.get("email")
        referrerTitle = self.request.get("referrerTitle")
        referrerfirstname = self.request.get("referrerfirstname")
        referrerlastname = self.request.get("referrerlastname")
        referrerContact = self.request.get("referrerContact")
        
        if self.request.get("trainingSession"):
            seleced_city = ndb.Key(urlsafe=self.request.get("trainingSession"))

        if self.request.get("churchOrganisation"):
            seleced_church = ndb.Key(urlsafe=self.request.get("churchOrganisation"))

        if title and firstName and lastname and idnumber and cellPhoneNumber:
            trainingMember = models.TrainingMember()
            trainingMember.title = title
            trainingMember.firstName = firstName
            trainingMember.lastname = lastname
            trainingMember.idnumber = idnumber
            trainingMember.cellPhoneNumber = cellPhoneNumber
            trainingMember.email = email

            if self.request.get("trainingSession"):
                trainingMember.city_id = seleced_city

            if referrerTitle and referrerfirstname and referrerlastname and referrerContact:
                trainingMember.referrerTitle = referrerTitle
                trainingMember.referrerfirstname = referrerfirstname
                trainingMember.referrerlastname = referrerlastname
                trainingMember.referrerContact = referrerContact

            if self.request.get("churchOrganisation"):
                trainingMember.church_id = seleced_church

            savedMember = True
            trainingMember.put()

            update_city = trainingMember.city_id.get()
            if update_city:
                updatedSlot = True
                update_city.available = update_city.available - 1
                update_city.put()

            lastname =  str(trainingMember.lastname)
            title =  str(trainingMember.title)   
            ref =  str(trainingMember.referenceNumber)  
            
            if savedMember == True and updatedSlot == True:
                tempNumber = trainingMember.cellPhoneNumber[1:]
                smsNumber = '27'+ tempNumber
                message = Utilities.getMessage(title,lastname,ref)
                sms.send(smsNumber,message)

            template = jinja_environment.get_template('templates/thank-you.html')
            self.response.out.write(template.render({'slots': slots, 'churches': churches}))

class LinkingMember(webapp2.RequestHandler):
    def post(self):
        slots = models.City.get_available_slots()
        churches = models.Church.get_available_churches()
        savedMember = False

        title = self.request.get("title")
        firstName = self.request.get("firstname")
        lastname = self.request.get("lastname")
        idnumber = self.request.get("idnumber")
        cellPhoneNumber = self.request.get("cellPhoneNumber")
        referrerTitle = self.request.get("referrerTitle")
        referrerfirstname = self.request.get("referrerfirstname")
        referrerlastname = self.request.get("referrerlastname")
        referrerContact = self.request.get("referrerContact")

        if self.request.get("churchOrganisation"):
            seleced_church = ndb.Key(urlsafe=self.request.get("churchOrganisation"))

        if title and firstName and lastname and idnumber and cellPhoneNumber:
            linkingMember = models.LinkingMember()
            linkingMember.title = title
            linkingMember.firstName = firstName
            linkingMember.lastname = lastname
            linkingMember.idnumber = idnumber
            linkingMember.cellPhoneNumber = cellPhoneNumber
            
            if referrerTitle and referrerfirstname and referrerlastname and referrerContact:
                linkingMember.referrerTitle = referrerTitle
                linkingMember.referrerfirstname = referrerfirstname
                linkingMember.referrerlastname = referrerlastname
                linkingMember.referrerContact = referrerContact
            
            if self.request.get("churchOrganisation"):
                linkingMember.church_id = seleced_church

            linkingMember.put()
            savedMember = True

            lastname =  str(linkingMember.lastname)
            title =  str(linkingMember.title)   
            ref =  str(linkingMember.referenceNumber)  
            
            if savedMember == True:
                tempNumber = linkingMember.cellPhoneNumber[1:]
                smsNumber = '27'+ tempNumber
                message = Utilities.getMessage(title,lastname,ref)
                sms.send(smsNumber,message)

        template = jinja_environment.get_template('templates/thank-you.html')
        self.response.out.write(template.render({'churches': churches}))

class SeminorMember(webapp2.RequestHandler):
    def post(self):
        churches = models.Church.get_available_churches()
        savedMember = False

        title = self.request.get("title")
        firstName = self.request.get("firstname")
        lastname = self.request.get("lastname")
        idnumber = self.request.get("idnumber")
        cellPhoneNumber = self.request.get("cellPhoneNumber")
        referrerTitle = self.request.get("referrerTitle")
        referrerfirstname = self.request.get("referrerfirstname")
        referrerlastname = self.request.get("referrerlastname")
        referrerContact = self.request.get("referrerContact")

        if self.request.get("churchOrganisation"):
            seleced_church = ndb.Key(urlsafe=self.request.get("churchOrganisation"))

        if title and firstName and lastname and idnumber and cellPhoneNumber:
            seminorMember = models.SeminorMember()
            seminorMember.title = title
            seminorMember.firstName = firstName
            seminorMember.lastname = lastname
            seminorMember.idnumber = idnumber
            seminorMember.cellPhoneNumber = cellPhoneNumber
            
            if referrerTitle and referrerfirstname and referrerlastname and referrerContact:
                seminorMember.referrerTitle = referrerTitle
                seminorMember.referrerfirstname = referrerfirstname
                seminorMember.referrerlastname = referrerlastname
                seminorMember.referrerContact = referrerContact
        
            if self.request.get("churchOrganisation"):
                seminorMember.church_id = seleced_church
        
            seminorMember.put()
            savedMember = True
            
            lastname =  str(seminorMember.lastname)
            title =  str(seminorMember.title)   
            ref =  str(seminorMember.referenceNumber)  
            
            if savedMember == True:
                tempNumber = seminorMember.cellPhoneNumber[1:]
                smsNumber = '27'+ tempNumber
                message = Utilities.getMessage(title,lastname,ref)
                sms.send(smsNumber,message)
            
        template = jinja_environment.get_template('templates/thank-you.html')
        self.response.out.write(template.render({'churches':churches}))
        
class AdminReportTraining(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        cursor = self.request.get("cursor", None)
        if cursor:
            cursor = ndb.Cursor(urlsafe=cursor)

        members, next_cursor, more = models.TrainingMember.query().fetch_page(100, start_cursor=cursor);
        result = {}
        result["cursor"] = next_cursor.urlsafe() if next_cursor else None
        result["more"] = more
        result["data"] = []
        for x in xrange(len(members)):
            member = members[x]

            if member.idnumber:
                d = {}
                d["title"] = member.title
                d["first_name"] = member.firstName
                d["last_name"] = member.lastname
                d["id_number"] = member.idnumber
                d["cellphone"] = member.cellPhoneNumber
                d["reference_number"] = member.referenceNumber
                d["reffered_by_name"] = member.referrerfirstname
                d["reffered_by_surname"] = member.referrerlastname
                d["reffered_by_contact"] = member.referrerContact
                d["email"] = member.email
                d["date"] = member.city_id.get().datetime.strftime("%d %B %Y %H:%M") if member.city_id else None
                d["city"] = member.city_id.get().cityName if member.city_id else None
                d["reffered_by_pastors_name"] = member.church_id.get().pasterName if member.church_id else None
                d["reffered_by_pastors_church_name"] = member.church_id.get().churchName if member.church_id else None
                d["reffered_by_pastors_address"] = member.church_id.get().address if member.church_id else None
                result["data"].append(d)
        self.response.out.write(json.dumps(result))

class AdminReportSeminor(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        cursor = self.request.get("cursor", None)
        if cursor:
            cursor = ndb.Cursor(urlsafe=cursor)

        members, next_cursor, more = models.SeminorMember.query().fetch_page(10, start_cursor=cursor);
        result = {}
        result["cursor"] = next_cursor.urlsafe() if next_cursor else None
        result["more"] = more
        result["data"] = []
        for x in xrange(len(members)):
            member = members[x]

            if member.idnumber:
                d = {}
                d["title"] = member.title
                d["first_name"] = member.firstName
                d["last_name"] = member.lastname
                d["id_number"] = member.idnumber
                d["cellphone"] = member.cellPhoneNumber
                d["reference_number"] = member.referenceNumber
                d["reffered_by_name"] = member.referrerfirstname
                d["reffered_by_surname"] = member.referrerlastname
                d["reffered_by_contact"] = member.referrerContact
                d["reffered_by_pastors_name"] = member.church_id.get().pasterName if member.church_id else None
                d["reffered_by_pastors_church_name"] = member.church_id.get().churchName if member.church_id else None
                d["reffered_by_pastors_address"] = member.church_id.get().address if member.church_id else None
                result["data"].append(d)
        self.response.out.write(json.dumps(result))

class AdminReportRegistration(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        cursor = self.request.get("cursor", None)
        if cursor:
            cursor = ndb.Cursor(urlsafe=cursor)

        members, next_cursor, more = models.RegistrationMember.query().fetch_page(10, start_cursor=cursor);
        result = {}
        result["cursor"] = next_cursor.urlsafe() if next_cursor else None
        result["more"] = more
        result["data"] = []
        for x in xrange(len(members)):
            member = members[x]

            if member.idnumber:
                d = {}
                d["title"] = member.title
                d["first_name"] = member.firstName
                d["last_name"] = member.lastname
                d["id_number"] = member.idnumber
                d["cellphone"] = member.cellPhoneNumber
                d["reffered_by_name"] = member.referrerfirstname
                d["reffered_by_surname"] = member.referrerlastname
                d["reffered_by_contact"] = member.referrerContact
                d["reffered_by_pastors_name"] = member.church_id.get().pasterName if member.church_id else None
                d["reffered_by_pastors_church_name"] = member.church_id.get().churchName if member.church_id else None
                d["reffered_by_pastors_address"] = member.church_id.get().address if member.church_id else None
                result["data"].append(d)
        self.response.out.write(json.dumps(result))

class AdminReportLinking(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        cursor = self.request.get("cursor", None)
        if cursor:
            cursor = ndb.Cursor(urlsafe=cursor)

        members, next_cursor, more = models.LinkingMember.query().fetch_page(10, start_cursor=cursor);
        result = {}
        result["cursor"] = next_cursor.urlsafe() if next_cursor else None
        result["more"] = more
        result["data"] = []
        for x in xrange(len(members)):
            member = members[x]

            if member.idnumber:
                d = {}
                d["title"] = member.title
                d["first_name"] = member.firstName
                d["last_name"] = member.lastname
                d["id_number"] = member.idnumber
                d["cellphone"] = member.cellPhoneNumber
                d["reference_number"] = member.referenceNumber
                d["reffered_by_name"] = member.referrerfirstname
                d["reffered_by_surname"] = member.referrerlastname
                d["reffered_by_contact"] = member.referrerContact
                d["reffered_by_pastors_name"] = member.church_id.get().pasterName if member.church_id else None
                d["reffered_by_pastors_church_name"] = member.church_id.get().churchName if member.church_id else None
                d["reffered_by_pastors_address"] = member.church_id.get().address if member.church_id else None
                result["data"].append(d)
        self.response.out.write(json.dumps(result))

class Utilities():
    @staticmethod
    def getMessage(title,lastname,ref): 
        message = title +'+' + lastname +',+' + 'Welcome+to+FX+Legacy.+' +'Your+reference+number+is:+'+ ref
        return message

    @staticmethod
    def getContactUsMessage(): 
        messageOne = 'FX+Legacy+-+Thank+you+for+filling+out+our+contact+us+form.+'  
        messageTwo = 'One+of+our+consultants+will+get+in+touch+with+you+shortly.'
        message = messageOne + messageTwo
        return message

class ContactUsForm(webapp2.RequestHandler):
    def post(self):

        name = self.request.get("name")
        tel = self.request.get("tel")
        email = self.request.get("email")
        message = self.request.get("message")
        
        sender = "kholekiletinzi@gmail.com"
        to = "kholekiletinzi@gmail.com"
        subject = "Contact Us Form"
        body =  "Name : "+ name +".\n" \
                "Email Address : "+ email +".\n" \
                "Phone Number : "+ tel +".\n" \
                "Message : " + message

        mail.send_mail(sender=sender,to=to,subject=subject,body=body)

        tempNumber = tel[1:]
        smsNumber = '27'+ str(tempNumber)
        smsMessage = Utilities.getContactUsMessage()
        sms.send(smsNumber,smsMessage)

        template = jinja_environment.get_template('templates/thankyou.html')
        self.response.out.write(template.render())
       
app = webapp2.WSGIApplication([ ('/', Home),
                                ('/about-us', About),
                                ('/services', Services),
                                ('/services/copy-trading', AutoTrading),
                                ('/services/forex-training', ForexTraining),
                                ('/services/forex-seminar', ForexSeminar),
                                ('/packages', ComparePackages),
                                ('/legal/terms-and-conditions', TermsAndConditions),
                                ('/legal/risk-warning', RiskWarning),
                                ('/legal/privacy-policy', PrivacyPolicy),
                                ('/contact-us', ContactUs),
                                ('/training-form', CreateTrainingMember),
                                ('/linking-form', LinkingMember),
                                ('/seminor-form', SeminorMember),
                                ('/contact-us-form', ContactUsForm),
                                ('/admin/report/training', AdminReportTraining),
                                ('/admin/report/seminor', AdminReportSeminor),
                                ('/admin/report/register', AdminReportRegistration),
                                ('/admin/report/linking', AdminReportLinking)
                                ],debug=False)