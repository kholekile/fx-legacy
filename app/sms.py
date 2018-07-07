from google.appengine.api import urlfetch
from google.appengine.ext import deferred
import urllib
import logging

def send_async(to_number, msg):
    deferred.defer(send, to_number, msg)

def send(to_number, msg):
    app_id = "CY1Tv-d8SOys3y7Hjt3Jfg=="
    url = "https://platform.clickatell.com/messages/http/send?apiKey="+app_id+"&to="+to_number+"&content="+msg
    result = urlfetch.fetch(url=url, method=urlfetch.GET)
    return result