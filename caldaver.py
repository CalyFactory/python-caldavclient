import requests 
import static


class CaldavClient:

    def __init__(self, hostname, id, pw):
        self.hostname = hostname
        self.userId = id
        self.userPw = pw 
    
    def getPrincipal(self):
        ret = self.request(
            depth = 0,
            data = static.XML_REQ_PRINCIPAL
        )
        print(ret.status_code)
        print(ret.text)

    def request(self, method = "PROPFIND", depth = 0, data = ""):
        response = requests.request(
            method,
            self.hostname,
            data = data, 
            headers = {
                "Depth" : str(depth)
            },
            auth = (
                self.userId, 
                self.userPw 
            )
        )
        return response

class Principal:
    
    def __init__(self, root, principal):
        self.root = root 
        self.principal = principal
        self.domain = root + principal
