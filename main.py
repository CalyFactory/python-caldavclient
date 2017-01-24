from caldaver import CaldavClient
import json 
import time 

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

a = {'a': 1, 'b': 1, 'c': 0}
b = {'a': 1, 'b': 2, 'd': 0}
d = DictDiffer(b, a)
print ("Added:" + str(d.added()))
print ("Removed:" + str(d.removed()))
print ("Changed:" + str(d.changed()))
print ("Unchanged:" + str(d.unchanged()))
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
for event in originEventList:
    print (event.eTag)

while True:
    print("start sync")
    changedList = principal.isListHasChanges(originCalendars)

    if len(changedList)!=0:
        print("change detected")
        for changeCalendar in changedList:
            print(changeCalendar)


    else:
        print("nothing changed")
    originCalendars = principal.getCalendars()

    time.sleep(10)
