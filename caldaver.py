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
            principalUrl = xmlTree[0][0].text
        )
        return principal

    class Principal:
        
        def __init__(self, hostname, principalUrl):
            self.hostname = util.getHostnameFromUrl(hostname)
            print(self.hostname)
            self.principalUrl = principalUrl
            self.domainUrl = hostname + principalUrl

        def getCalendars(self):
            ret = util.requestData(
                hostname = self.domainUrl,
                depth = 0,
                data = static.XML_REQ_HOMESET,
                auth = self.auth
            )
            print(ret)

    class VCalendar:

        def __init__(self, hostname, vcalendarUrl):
            self.hostname = hostname
            self.vcalendarUrl = vcalendarUrl
            self.domainUrl = hostname + vcalendarUrl
        