import requests 

class CaldavClient:

    def __init__(self, hostname, id, pw):
        self.hostname = hostname
        self.userId = id
        self.userPw = pw 
    
    def getPrincipal(self):
        ret = requests.request(
            "PROPFIND",
            self.hostname, 
            data = (
                "<?xml version='1.0' encoding='utf-8'?>"
                "<ns0:propfind xmlns:C=\"urn:ietf:params:xml:ns:caldav\" xmlns:D=\"DAV\" xmlns:ns0=\"DAV:\">"
                "   <ns0:prop>"
                "       <C:calendar-home-set/>"
                "   </ns0:prop>"
                "</ns0:propfind>"
            ),
            auth = (
                self.userId,
                self.userPw
            )
        )
        print(ret.status_code)
        print(ret.text) 