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
            principalUrl = xmlTree.find(".//{DAV:}response")
                                    .find(".//{DAV:}propstat")
                                    .find(".//{DAV:}prop")
                                    .find(".//{DAV:}current-user-principal")
                                    .find(".//{DAV:}href").text,
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
            
            calendarUrl = (
                xmlTree.find(".//{DAV:}response")
                        .find(".//{DAV:}propstat")
                        .find(".//{DAV:}prop")
                        .find(".//{urn:ietf:params:xml:ns:caldav}calendar-home-set")
                        .find(".//{DAV:}href").text
            )

            ## load calendar info (name, id, ctag)
            ret = util.requestData(
#                hostname = self.hostname + calendarUrl,
                hostname = calendarUrl,
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
                    calendarUrl = response.find("href").text,
                    calendarName = response.find(".//{DAV:}propstat")
                                    .find(".//{DAV:}prop")
                                    .find(".//{DAV:}display-name").text,
                    cTag = response.find(".//{DAV:}propstat")
                            .find(".//{DAV:}prop")
                            .find(".//{DAV:}getctag").text,
                    client = self.client
                )
                calendarList.append(calendar)
            return calendarList
        
        def isListHasChanges(self, calendarList):
            newCalendarList = self.getCalendars()
            
            newCalendarDict = util.calListToDict(newCalendarList)
            calendarDict = util.calListToDict(calendarList)
            dictDiffer = util.DictDiffer(newCalendarDict, calendarDict)
            

            return dictDiffer.changed()

    class Calendar:

        def __init__(self, calendarUrl, cTag, client):
            self.hostname = util.getHostnameFromUrl(client.hostname)
            self.calendarUrl = calendarUrl
            self.cTag = cTag
            self.eventList = []
            self.domainUrl = self.hostname + calendarUrl
            self.client = client

        def __init__(self, hostname, calendarUrl, calendarName, cTag, client):
            self.hostname = util.getHostnameFromUrl(hostname)
            self.calendarUrl = calendarUrl
            self.calendarName = calendarName
            self.eventList = []
            self.cTag = cTag
            self.domainUrl = self.hostname + calendarUrl
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

            #save event data
            self.eventList = eventList
            return eventList

        ## TODO - ctag만 불러올 수 있는 쿼리 찾아보기
        def getCTag(self):
            ## load ctag
            ret = util.requestData(
                hostname = self.domainUrl,
                depth = 1,
                data = static.XML_REQ_CALENDARCTAG,
                auth = self.client.auth
            )

    class Event:
        def __init__(self, eventUrl, eTag):
            self.eventUrl = eventUrl
            self.eTag = eTag