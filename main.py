from caldaver import CaldavClient
import json 

with open('key.json') as json_data:
    d = json.load(json_data)
    userId = d['naver']['id']
    userPw = d['naver']['pw']

# naver : https://caldav.calendar.naver.com:443/caldav/jspiner/calendar/
# apple : caldav.icloud.com

client = CaldavClient(
#    "https://caldav.icloud.com:443",
    "https://caldav.calendar.naver.com:443/caldav/jspiner/calendar/",
    userId,
    userPw
)

print(client.getPrincipal())