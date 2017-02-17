from caldavclient import CaldavClient
import json 
import time 
from caldavclient import util

with open('key.json') as json_data:
    d = json.load(json_data)
    userId = d['naver']['id']
    userPw = d['naver']['pw']

# naver : https://caldav.calendar.naver.com:443/caldav/jspiner/calendar/
# apple : caldav.icloud.com

##calendar load example 
client = CaldavClient(
#    "https://caldav.icloud.com",
    "https://caldav.calendar.naver.com/principals/",
    (userId, userPw)
)

principal = client.getPrincipal()
homeset = principal.getHomeSet()
calendars = homeset.getCalendars()

for calendar in calendars:
    print(calendar.calendarName + " " + calendar.calendarUrl + " " + calendar.cTag)

eventList = calendars[0].getAllEvent()
for event in eventList:
    print (event.eTag)


"""
##calendar sync example(new)

#client 객체에 db에서 데이터를 불러와 넣어줌 
client = (
    CaldavClient(
        hostname,
        userId,
        userPw
    ).setPrincipal("principal_url")   #db 에서 로드 
    .setHomeSet("home_set_cal_url")  #db 에서 로드 
    .setCalendars("calendarList")       #db에서 로드해서 list calendar object 로 삽입
)

calendars = client.getPrincipal().getHomeSet().getCalendars()

## 주기적으로 돌면서 diff 체크 
while True:
    print("start sync")

    ##동기화할 캘린더 선택 
    calendarToSync = calendars[0]
    if calendarToSync.isChanged():
        print("something changed")
        newEventList = calendarToSync.updateAllEvent()
        oldEventList = [] #db에서 이전 event리스트들을 불러옴 
        eventDiff = util.diffEvent(newEventList, oldEventList)

        
        print("add : " + str(eventDiff.added()))
        print("removed : " + str(eventDiff.removed()))
        print("changed : " + str(eventDiff.changed()))
        print("unchanged : " + str(eventDiff.unchanged()))
    else:
        print("nothing changed")

    

    time.sleep(10)
"""




##calendar sync example(old)
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