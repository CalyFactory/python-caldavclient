import sys
# Add the ptdraft folder path to the sys.path list

import requests
from urllib.parse import urlparse
from xml.etree.ElementTree import *
from caldavclient import caldavclient
from datetime import datetime
import json
from icalendar import Calendar

def requestData(method = "PROPFIND", hostname = "", depth = 0, data = "", auth = ("","")):
    if isinstance(auth, tuple):
        response = requests.request(
            method,
            hostname,
            data = data, 
            headers = {
                "Depth" : str(depth)
            },
            auth = auth 
        )
    else:
        response = requests.request(
            method,
            hostname,
            data = data, 
            headers = {
                "Depth" : str(depth),
                "Authorization" : "Basic " + str(auth)
            },
        )

    if response.status_code<200 or response.status_code>299:
        raise Exception('http code error' + str(response.status_code))

    return response

# Convert ics to json format
def convert_ics_to_json(homeset_cal_id, cal_id, evt_id, acc_auth): # acc_auth="Basic user_base64_hash_key"
    # Open .ics
    url_resp = requests.request("GET",homeset_cal_id+cal_id+evt_id,headers={"Depth":"1","Authorization":"Basic "+acc_auth})
    cal = Calendar.from_ical(url_resp.text)
    for component in cal.walk():
        if component.name == "VEVENT":
            evt_name=component.get('summary')
            dt_start=str(component.get('dtstart').dt)
            dt_end=str(component.get('dtend').dt)
            location=component.get('location')

            dt_start=dtConverter(dt_start)
            dt_end=dtConverter(dt_end)

            return json.dumps({
                    'name': evt_name,
                    'dt_start': dt_start,
                    'dt_end': dt_end,
                    'location': location
                })
    return "error"

# Convert with home-set-calendar ID
def convert_ics_to_json_with_hscalID(homeset_cal_id, cal_id, evt_id):
    res = db_connector.query("select user_base64 from account where home_set_cal_url=%s",(homeset_cal_id,))
    rows = util.fetch_all_json(res)
    if rows[0]['user_base64'] is None:
        return #handle error message
    acc_auth=rows[0]['user_base64']
    convert_ics_to_json(homeset_cal_id, cal_id, evt_id, acc_auth)


def dtConverter(dt_ics):
    # ICS Date time format : TZID=Asia/Seoul:20170117T090000
    # iCalendar Date time format : 2017-01-17 10:00:00+09:00
    
    # how to handle korean time?

    return dt_ics

def getHostnameFromUrl(url):
    parsedUrl = urlparse(url)
    hostname = '{uri.scheme}://{uri.netloc}'.format(uri=parsedUrl)
    return hostname

def mixHostUrl(hostname, url):
    if "http://" in url or "https://" in url:
        return url
    else:
        return hostname + url

def splitIdfromUrl(url):
    if len(url) < 1:
        return url
    url = url.replace('.ics', '')
    if url[-1] == "/":
        url = url[:-1]
    return url.split('/')[-1]    

class XmlObject:

    def __init__(self, xml = None):
        if xml == None:
            self.root = None
        elif isinstance(xml, Element):
            self.root = xml
        else:
            self.root = ElementTree(fromstring(xml)).getroot()
    
    def addNamespace(self, tag):
        if tag == "calendar-home-set":
            tag = ".//{urn:ietf:params:xml:ns:caldav}" + tag
        elif tag == "calendar-data":
            tag = ".//{urn:ietf:params:xml:ns:caldav}" + tag
        elif tag == "getctag":
            tag = ".//{http://calendarserver.org/ns/}" + tag
        else:
            tag = ".//{DAV:}" + tag
        return tag

    def find(self, tag):
        tag = self.addNamespace(tag)

        childObject = self.root.find(tag)
        if childObject == None:
            return XmlObject()
        return XmlObject(childObject)
    
    def iter(self):
        elementList = []
        for element in self.root:
            elementList.append(XmlObject(element))
        return elementList
    
    def text(self):
        if self.root==None:
            return ""
        else:
            return self.root.text
    

class DictDiffer(object):
    def __init__(self, past_dict, current_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect 

    def removed(self):
        return self.set_past - self.intersect 

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def calListToDict(calendarList):
    calDict = {}
    for calendar in calendarList:
        calDict[calendar.calendarUrl] = calendar.cTag
    return calDict

def eventListToDict(eventList):
    eventDict = {}
    for event in eventList:
        eventDict[event.eventUrl] = event.eTag
    return eventDict

def eventRowToList(eventRow):
    eventList = []
    for row in eventRow:
        event = caldavclient.CaldavClient.Event(
            eventUrl = row['event_url'],
            eTag = row['e_tag']
        )
        eventList.append(event)
    return eventList

def findETag(eventList, eventUrl):
    for event in eventList:
        if event.eventUrl == eventUrl:
            if event.eTag is None:
                return ""
            return event.eTag

def findCalendar(key, list):
    for calendar in list:
        if calendar.calendarUrl == key:
            return calendar

def diffCalendars(oldList, newList):
    diffList = []
    for calendar in oldList:
        newCalendar = findCalendar(calendar.calendarUrl, newList)
        if newCalendar.cTag != calendar.cTag:
            diffList.append([calendar, newCalendar])
    return diffList

def diffEvent(oldList, newList):
    return DictDiffer(
        eventListToDict(oldList), 
        eventListToDict(newList)
    )

def fetch_all_json(result):
  lis = []

  for row in result.fetchall():
    i =0
    dic = {}  
    
    for data in row:
      if type(data) == datetime:
        dic[result.keys()[i]]= str(data)
      else:
        dic[result.keys()[i]]= data
      if i == len(row)-1:
        lis.append(dic)

      i=i+1
  return lis