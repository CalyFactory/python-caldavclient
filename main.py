from caldaver import CaldavClient
import json 
import time 
import util

with open('key.json') as json_data:
    d = json.load(json_data)
    userId = d['naver']['id']
    userPw = d['naver']['pw']

# naver : https://caldav.calendar.naver.com:443/caldav/jspiner/calendar/
# apple : caldav.icloud.com

"""
##calendar load example 
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

"""


##calendar sync example

client = CaldavClient(
    "https://caldav.calendar.naver.com/principals/users/jspiner",
    userId,
    userPw
)

principal = client.getPrincipal()
originCalendars = principal.getCalendars()

for calendar in originCalendars:
    print(calendar.calendarName + " " + calendar.calendarUrl + " " + calendar.cTag)

originEventList = originCalendars[0].getAllEvent()
for event in originCalendars[0].eventList:
    print (event.eTag)

while True:
    print("start sync")
    newCalendars = principal.getCalendars()
    
    changedList = util.diffCalendar(newCalendars, originCalendars)

    if len(changedList)!=0:
        print("change detected")
        for old, new in changedList:
            print(old)
            print(new)
            print(old.eventList)
            print(new.eventList)
            
            eventDiff = util.diffEvent(old.eventList, new.getAllEvent())
            print("add : " + eventDiff.added())
            print("removed : " + eventDiff.removed())
            print("changed : " + eventDiff.changed())
            print("unchanged : " + eventDiff.unchanged())

    else:
        print("nothing changed")


    originCalendars = newCalendars
    time.sleep(10)
