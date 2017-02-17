# Python Calendaring Extensions to WebDAV library
caldav library

Support 
------------
 - Basic Auth (Http 1.1)
 - Xml Req
 - Get Principal Info
 - Get HomeSet Info
 - Get cTag, eTag, calendar event Info
 - Diff with cached data(ctag, etag)
 - ICS Parsing
 
Basic Useage
------------
```python
##calendar load example 
client = CaldavClient(
    hostname,
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
```

This sample will show this result.
```
내 캘린더 /caldav/jspiner/calendar/<calendarId>/ 2017-01-24 21:15:19
내 할 일 /caldav/jspiner/calendar/<calendarId>/ 2013-11-22 17:14:01

"2017-01-24 21:15:16"
"2017-01-24 21:15:13"
"2017-01-22 17:13:18"
"2015-11-09 20:24:01"
"2015-10-28 01:58:56"
"2015-10-08 00:03:03"
"2015-10-07 03:47:20"
"2015-10-06 12:06:37"
...
```


CalDav Server
------------

- Naver : https://caldav.calendar.naver.com/principals/
- apple : https://caldav.apple.com
- Google : I recommend using its own api.
- yahoo : https://caldav.calendar.yahoo.com
