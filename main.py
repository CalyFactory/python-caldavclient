from caldavclient import CaldavClient
import json 
import time 
from caldavclient import util

with open('key.json') as json_data:
    d = json.load(json_data)
    userId = d['naver2']['id']
    userPw = d['naver2']['pw']

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

eventList = calendars[0].getEventByRange( "20161117T000000Z", "20170325T000000Z")
eventDataList = calendars[0].getCalendarData(eventList)
data = eventDataList[0].eventData
print(data)
for event in eventDataList:
    print (event.eventData)
    print("===")


data = (
"""
BEGIN:VCALENDAR
PRODID:-//NHN Corp//Naver Calendar 1.0//KO
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VTIMEZONE
TZID:Asia/Seoul
TZURL:http://tzurl.org/zoneinfo-outlook/Asia/Seoul
X-LIC-LOCATION:Asia/Seoul
BEGIN:STANDARD
TZOFFSETFROM:+0900
TZOFFSETTO:+0900
TZNAME:KST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
CREATED:20141126T034341Z
LAST-MODIFIED:20141126T034341Z
DTSTAMP:20170221T071734Z
UID:35BC4AF5-2376-4473-A422-D63366885BB2:88_ios_import
TRANSP:TRANSPARENT
STATUS:TENTATIVE
SEQUENCE:0
SUMMARY:추석 연휴
DESCRIPTION:
DTSTART;VALUE=DATE:20160916
DTEND;VALUE=DATE:20160917
CLASS:PUBLIC
LOCATION:
PRIORITY:5
X-NAVER-STICKER-ID:001
X-NAVER-STICKER-POS:0
X-NAVER-STICKER-DEFAULT-POS:1
X-NAVER-CATEGORY-ID:0
X-NAVER-SCHEDULE-DETAIL-VIEW-URL:https://calendar.naver.com/calapp/main.nhn#HistoryData=%7B%22sType%22%3A%22Layer%22%2C%22sUIO%22%3A%22ViewSchedule%22%2C%22sCalendarId%22%3A%225272575%22%2C%22sScheduleId%22%3A%22692595578%22%2C%22nScheduleType%22%3A2%2C%22sStartDate%22%3A%222016-09-16%2000%3A00%3A00%22%7D
X-NAVER-WRITER-ID:kkk1140
END:VEVENT
END:VCALENDAR
"""
)
"""
from icalendar import Calendar, Event
import icalendar
calendar = Calendar.from_ical(data)
for component in calendar.walk():
    if component.name == "VEVENT":
        for row in component.property_items():
            if isinstance(row[1], icalendar.prop.vDDDTypes):
                result = component.decoded(row[0])
                print(str(row[0]) + " : " + str(type(result)) + " // " + str(result))
            else:
                print(str(row[0]) + " : " + str(row[1]))
"""

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