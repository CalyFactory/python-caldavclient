from caldavclient import static
from xml.etree.ElementTree import *
from caldavclient import util

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

#        xmlTree = ElementTree(fromstring(ret.content)).getroot()
        xmlTree = util.XmlObject(ret.content)

        principal = self.Principal(
            hostname = self.hostname,
            principalUrl = xmlTree.find("response")
                                .find("propstat")
                                .find("prop")
                                .find("current-user-principal")
                                .find("href").text(),
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

#            xmlTree = ElementTree(fromstring(ret.content)).getroot()
            xmlTree = util.XmlObject(ret.content)
            
            calendarUrl = (
                xmlTree.find("response")
                        .find("propstat")
                        .find("prop")
                        .find("calendar-home-set")
                        .find("href").text()
            )

            ## load calendar info (name, id, ctag)
            ret = util.requestData(
                hostname = util.mixHostUrl(self.hostname, calendarUrl),
                depth = 1,
                data = static.XML_REQ_CALENDARINFO,
                auth = self.client.auth
            )


#            xmlTree = ElementTree(fromstring(ret.content)).getroot()
            xmlTree = util.XmlObject(ret.content)

            calendarList = []
            for response in xmlTree.iter():
                if response.find("href").text() == calendarUrl:
                    continue
                calendar = self.client.Calendar(
                    hostname = self.hostname,
                    calendarUrl = response.find("href").text(),
                    calendarName = response.find("propstat")
                                    .find("prop")
                                    .find("displayname").text(),
                    cTag = response.find("propstat")
                            .find("prop")
                            .find("getctag").text(),
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
        
#            xmlTree = ElementTree(fromstring(ret.content)).getroot()
            xmlTree = util.XmlObject(ret.content)

            eventList = []
            for response in xmlTree.iter():
                if response.find("href").text == self.calendarUrl:
                    continue
                event = self.client.Event(
                    eventUrl = response.find("href").text(),
                    eTag = response.find("propstat").find("prop").find("getetag").text()
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