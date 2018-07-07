from google.appengine.ext import ndb
import random
import datetime

class Church(ndb.Model):
    churchName = ndb.StringProperty(default="")
    pasterName = ndb.StringProperty(default="")
    address = ndb.StringProperty(default="")

    def get_church_name(self):
        return self.churchName

    def get_paster_name(self):
        return self.pasterName

    def get_address(self):
        return self.address

    @staticmethod
    def get_available_churches():
        return Church.query().fetch()
        
class City(ndb.Model):
    datetime = ndb.DateTimeProperty(auto_now_add=True)
    cityName = ndb.StringProperty(default="")
    available = ndb.IntegerProperty(default=100)

    def get_day(self):
        return self.datetime.strftime("%A")

    def get_date(self):
        return self.datetime.strftime("%dth %b")

    def get_time(self):
        return self.datetime.strftime("%H:%M")

    def get_city_name(self):
        return self.cityName

    @staticmethod
    def get_available_slots():
        slots = City.query().filter(City.available > 0).fetch()
        return slots

class TrainingMember(ndb.Model):
    title = ndb.StringProperty(default="")
    firstName = ndb.StringProperty(default="")
    lastname = ndb.StringProperty(default="")
    idnumber = ndb.StringProperty(default="")
    cellPhoneNumber = ndb.StringProperty(default="")
    email = ndb.StringProperty(default="")
    referrerTitle = ndb.StringProperty(default="")
    referrerfirstname = ndb.StringProperty(default="")
    referrerlastname = ndb.StringProperty(default="")
    referrerContact = ndb.StringProperty(default="")
    referenceNumber = ndb.StringProperty(default="")
    city_id = ndb.KeyProperty(kind=City)
    church_id = ndb.KeyProperty(kind=Church)

    def __init__(self):
        super(TrainingMember, self).__init__()
        self.referenceNumber = 'TM'+str(int(random.random() * 9999)).rjust(4, "0")

class LinkingMember(ndb.Model):
    title = ndb.StringProperty(default="")
    firstName = ndb.StringProperty(default="")
    lastname = ndb.StringProperty(default="")
    idnumber = ndb.StringProperty(default="")
    cellPhoneNumber = ndb.StringProperty(default="")
    referrerTitle = ndb.StringProperty(default="")
    referrerfirstname = ndb.StringProperty(default="")
    referrerlastname = ndb.StringProperty(default="")
    referrerContact = ndb.StringProperty(default="")
    referenceNumber = ndb.StringProperty(default="")
    church_id = ndb.KeyProperty(kind=Church)

    def __init__(self):
        super(LinkingMember, self).__init__()
        self.referenceNumber = 'LM'+str(int(random.random() * 9999)).rjust(4, "0")

class SeminorMember(ndb.Model):
    title = ndb.StringProperty(default="")
    firstName = ndb.StringProperty(default="")
    lastname = ndb.StringProperty(default="")
    idnumber = ndb.StringProperty(default="")
    cellPhoneNumber = ndb.StringProperty(default="")
    referrerTitle = ndb.StringProperty(default="")
    referrerfirstname = ndb.StringProperty(default="")
    referrerlastname = ndb.StringProperty(default="")
    referrerContact = ndb.StringProperty(default="")
    referenceNumber = ndb.StringProperty(default="")
    church_id = ndb.KeyProperty(kind=Church)

    def __init__(self):
        super(SeminorMember, self).__init__()
        self.referenceNumber = 'SM'+str(int(random.random() * 9999)).rjust(4, "0")