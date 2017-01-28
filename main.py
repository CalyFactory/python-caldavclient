from caldavclient import CaldavClient
import json 
import time 
from caldavclient import util

with open('key.json') as json_data:
    d = json.load(json_data)
    userId = d['apple']['id']
    userPw = d['apple']['pw']

# naver : https://caldav.calendar.naver.com:443/caldav/jspiner/calendar/
# apple : caldav.icloud.com

##calendar load example 
client = CaldavClient(
    "https://caldav.icloud.com",
#    "https://caldav.calendar.naver.com/principals/users/jspiner",
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




##calendar sync example
"""
client = CaldavClient(
    "https://caldav.calendar.naver.com/principals/users/jspiner",
    userId,
    userPw
)

principal = client.getPrincipal()
originCalendars = principal.getCalendars()

originCalendars[0].getAllEvent()
originCalendars[1].getAllEvent()

for calendar in originCalendars:
    print(calendar.calendarName + " " + calendar.calendarUrl + " " + calendar.cTag)

originEventList = originCalendars[0].getAllEvent()
for event in originCalendars[0].eventList:
    print (event.eTag)

while True:
    print("start sync")
    newCalendars = principal.getCalendars()
    newCalendars[0].getAllEvent()
    newCalendars[1].getAllEvent()
    
    changedList = util.diffCalendar(originCalendars, newCalendars)

    if len(changedList)!=0:
        print("change detected")
        for old, new in changedList:
            
            eventDiff = util.diffEvent(old.eventList, new.eventList)
            print("add : " + str(eventDiff.added()))
            print("removed : " + str(eventDiff.removed()))
            print("changed : " + str(eventDiff.changed()))
            print("unchanged : " + str(eventDiff.unchanged()))

    else:
        print("nothing changed")


    originCalendars = newCalendars
    time.sleep(10)
"""