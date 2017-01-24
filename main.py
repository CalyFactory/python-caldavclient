from caldaver import CaldavClient
import json 

with open('key.json') as json_data:
    d = json.load(json_data)
    userId = d['naver']['id']
    userPw = d['naver']['pw']

# naver : https://caldav.calendar.naver.com:443/caldav/jspiner/calendar/
# apple : caldav.icloud.com

client = CaldavClient(
    "https://caldav.calendar.naver.com/principals/users/jspiner",
    userId,
    userPw
)

principal = client.getPrincipal()
calendars = principal.getCalendars()

for calendar in calendars:
    print(calendar.calendarName + " " + calendar.calendarUrl + " " + calendar.cTag)

eventList = calendars[0].getAllEvent()
for event in eventList:
    print (event.eTag)