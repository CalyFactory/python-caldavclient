from caldavclient import static
from xml.etree.ElementTree import *
from caldavclient import util

class CaldavClient:

    def __init__(self, hostname, id, pw):
        self.hostname = hostname
        self.auth = (id, pw)
        self.principal = None
    
    def getPrincipal(self):
        if self.principal is None:
            self.updatePrincipal()
        return self.principal
    
    def updatePrincipal(self):
        ret = util.requestData(
            hostname = self.hostname,
            depth = 0,
            data = static.XML_REQ_PRINCIPAL,
            auth = self.auth
        )

#        xmlTree = ElementTree(fromstring(ret.content)).getroot()
        xmlTree = util.XmlObject(ret.content)
        xmlTree.find("response").text
        
        principal = self.Principal(
            hostname = self.hostname,
            principalUrl = xmlTree.find("response")
                                .find("propstat")
                                .find("prop")
                                .find("current-user-principal")
                                .find("href").text(),
            client = self
        )
        self.principal = principal
        return principal
    
    def setPrincipal(self, principal):
        self.principal = self.Principal(
            hostname = self.hostname,
            principalUrl = principal,
            client = self
        )
        return self
    
    def setHomeSet(self, homeset):
        if self.principal == None:
            raise Exception('principal is not inited')
        else:
            self.principal.homeset = self.HomeSet(
                hostname = self.principal.hostname,
                homesetUrl = homeset,
                client = self
            )
        return self
            
    def setCalendars(self, calendarList):
        if self.principal == None:
            raise Exception('principal is not inited')
        elif self.principal.homeset == None:
            raise Exception('homeset is not inited')
        else:
            for calendar in calendarList:
                calendar.hostname = self.principal.homeset.hostname
                calendar.domainUrl = calendar.hostname + calendar.calendarUrl
                calendar.client = self 
            self.principal.homeset.calendarList = calendarList 
        return self 

    class Principal:
        
        def __init__(self, hostname, principalUrl, client):
            self.hostname = util.getHostnameFromUrl(hostname)
            self.principalUrl = principalUrl
            self.domainUrl = self.hostname + self.principalUrl
            self.client = client
            self.homeset = None 

        def getHomeSet(self):
            if self.homeset is None:
                self.updateHomeSet()
            return self.homeset
        
        def updateHomeSet(self):
            ## load calendar url 
            ret = util.requestData(
                hostname = self.domainUrl,
                depth = 0,
                data = static.XML_REQ_HOMESET,
                auth = self.client.auth
            )

#            xmlTree = ElementTree(fromstring(ret.content)).getroot()
            xmlTree = util.XmlObject(ret.content)
            
            homeset = self.client.HomeSet(
                hostname = self.hostname,
                homesetUrl = xmlTree.find("response")
                        .find("propstat")
                        .find("prop")
                        .find("calendar-home-set")
                        .find("href").text(),
                client = self.client
            )
            self.homeset = homeset
            return homeset
        
        def isListHasChanges(self, calendarList):
            newCalendarList = self.getCalendars()
            
            newCalendarDict = util.calListToDict(newCalendarList)
            calendarDict = util.calListToDict(calendarList)
            dictDiffer = util.DictDiffer(newCalendarDict, calendarDict)
            

            return dictDiffer.changed()
    
    class HomeSet:
        def __init__(self, hostname, homesetUrl, client):
            self.hostname = util.getHostnameFromUrl(homesetUrl)
            self.homesetUrl = homesetUrl
            self.client = client
            self.calendarList = None 

        def getCalendars(self):
            if self.calendarList is None:
                self.updateCalendars()
            return self.calendarList
        
        def updateCalendars(self):
            ## load calendar info (name, id, ctag)
            ret = util.requestData(
                hostname = util.mixHostUrl(self.hostname, self.homesetUrl),
                depth = 1,
                data = static.XML_REQ_CALENDARINFO,
                auth = self.client.auth
            )

#            xmlTree = ElementTree(fromstring(ret.content)).getroot()
            xmlTree = util.XmlObject(ret.content)

            calendarList = []
            for response in xmlTree.iter():
                if response.find("href").text() == self.homesetUrl:
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
            self.calendarList = calendarList
            return calendarList
            

    class Calendar:
        """
        def __init__(self, calendarUrl, calendarName, cTag):
#            self.hostname = util.getHostnameFromUrl(hostname)
            self.calendarId = util.splitIdfromUrl(calendarUrl)
            self.calendarUrl = calendarUrl
            self.calendarName = calendarName
            self.cTag = cTag
#            self.domainUrl = self.hostname + calendarUrl
#            self.client = client
            self.eventList = None
        """

        def __init__(self, calendarUrl, calendarName, cTag, client = None, hostname = None):
            self.hostname = util.getHostnameFromUrl(calendarUrl)
            self.calendarId = util.splitIdfromUrl(calendarUrl)
            self.calendarUrl = calendarUrl
            self.calendarName = calendarName
            self.cTag = cTag
            self.domainUrl = self.hostname + calendarUrl
            self.client = client
            self.eventList = None


        def isChanged(self):
            oldcTag = self.cTag 
            newcTag = self.getCTag()
            return oldcTag != newcTag
        
        def getAllEvent(self):
            if self.eventList is None:
                self.updateAllEvent()
            return self.eventList
        
        def updateAllEvent(self):
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

        def getCTag(self):
            ## load ctag
            ret = util.requestData(
                hostname = self.domainUrl,
                depth = 1,
                data = static.XML_REQ_CALENDARCTAG,
                auth = self.client.auth
            )

            xmlTree = util.XmlObject(ret.content)
            cTag = xmlTree.find("response").find("propstat").find("prop").find("getctag").text()
            self.cTag = cTag
            return cTag

    class Event:
        def __init__(self, eventUrl, eTag):
            self.eventUrl = eventUrl
            self.eventId = util.splitIdfromUrl(eventUrl)
            self.eTag = eTag