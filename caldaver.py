import static
from xml.etree.ElementTree import *
import util

class CaldavClient:

    def __init__(self, hostname, id, pw):
        self.hostname = hostname
        self.auth = (id, pw)
    
    def getPrincipal(self):
        ret = util.requestData(
            hostname = self.hostname,
            depth = 0,
            data = static.XML_REQ_PRINCIPAL,
            auth = self.auth
        )

        xmlTree = ElementTree(fromstring(ret.text)).getroot()
        
        principal = self.Principal(
            hostname = self.hostname,
            principalUrl = xmlTree[0][0].text,
            client = self
        )
        return principal

    class Principal:
        
        def __init__(self, hostname, principalUrl, client):
            self.hostname = util.getHostnameFromUrl(hostname)
            self.principalUrl = principalUrl
            self.domainUrl = self.hostname + self.principalUrl
            self.client = client

        def getCalendars(self):
            ## load calendar url 
            ret = util.requestData(
                hostname = self.domainUrl,
                depth = 0,
                data = static.XML_REQ_HOMESET,
                auth = self.client.auth
            )

            xmlTree = ElementTree(fromstring(ret.text)).getroot()

            calendarUrl = xmlTree[0][1][0][0][0].text

            ## load calendar info (name, id, ctag)
            ret = util.requestData(
                hostname = self.hostname + calendarUrl,
                depth = 1,
                data = static.XML_REQ_CALENDARINFO,
                auth = self.client.auth
            )


            xmlTree = ElementTree(fromstring(ret.text)).getroot()

            calendarList = []
            for response in xmlTree:
                if response[0].text == calendarUrl:
                    continue
                calendar = self.client.Calendar(
                    hostname = self.hostname,
                    calendarUrl = response[0].text,
                    calendarName = response[1][0][1].text,
                    cTag = response[1][0][2].text,
                    client = self.client
                )
                calendarList.append(calendar)
            return calendarList

    class Calendar:

        def __init__(self, hostname, calendarUrl, calendarName, cTag, client):
            self.hostname = util.getHostnameFromUrl(hostname)
            self.calendarUrl = calendarUrl
            self.calendarName = calendarName
            self.cTag = cTag
            self.domainUrl = hostname + calendarUrl
            self.client = client
        
        def getAllEvent(self):
            ## load all event (etag, info)
            ret = util.requestData(
                hostname = self.domainUrl,
                depth = 1,
                data = static.XML_REQ_CALENDARETAG,
                auth = self.client.auth
            )
        
            xmlTree = ElementTree(fromstring(ret.text)).getroot()
            eventList = []
            for response in xmlTree:
                if response[0].text == self.calendarUrl:
                    continue
                event = self.client.Event(
                    eventUrl = response[0].text,
                    eTag = response[1][0][0].text
                )
                eventList.append(event)
            
            return eventList

    class Event:
        def __init__(self, eventUrl, eTag):
            self.eventUrl = eventUrl
            self.eTag = eTag