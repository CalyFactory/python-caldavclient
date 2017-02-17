
#################################################
#                                               #
#      PROPFIND RQEUST BODY XML                 #
#                                               #
#################################################

XML_REQ_PRINCIPAL = (

    "<D:propfind xmlns:D='DAV:'> "
    "<D:prop> "
    "    <D:current-user-principal/> "
    "</D:prop> "
    "</D:propfind> "
)

XML_REQ_HOMESET = (
    "<?xml version='1.0' encoding='utf-8'?>"
    "<ns0:propfind xmlns:C=\"urn:ietf:params:xml:ns:caldav\" xmlns:D=\"DAV\" xmlns:ns0=\"DAV:\">"
    "   <ns0:prop>"
    "       <C:calendar-home-set/>"
    "   </ns0:prop>"
    "</ns0:propfind>"
)

XML_REQ_CALENDARINFO = (
    "<?xml version='1.0' encoding='utf-8'?>"
    "<ns0:propfind xmlns:C=\"urn:ietf:params:xml:ns:caldav\" xmlns:D=\"DAV\" xmlns:ns0=\"DAV:\"  xmlns:cs=\"http://calendarserver.org/ns/\">"
    "   <ns0:prop>"
    "       <ns0:resourcetype/>"
    "       <ns0:displayname />"
    "       <cs:getctag />"
    "   </ns0:prop>"
    "</ns0:propfind>"
)

XML_REQ_CALENDARCTAG = (
    "<?xml version='1.0' encoding='utf-8'?>"
    "<d:propfind xmlns:d=\"DAV:\" xmlns:cs=\"http://calendarserver.org/ns/\">"
    "   <d:prop>"
    "      <cs:getctag />"
    "   </d:prop>"
    "</d:propfind>"
)

XML_REQ_CALENDARETAG = (
    "<?xml version='1.0' encoding='utf-8'?>"
    "<d:propfind xmlns:d=\"DAV:\" xmlns:c=\"urn:ietf:params:xml:ns:caldav\">"
    "   <d:prop>"
    "       <d:getetag />"
    "       <c:calendar-data />"
    "   </d:prop>"
    "   <d:filter>"
    "       <c:comp-filter name=\"VCALENDAR\" />"
    "   </d:filter>"
    "</d:propfind>"
)

XML_REQ_CALENDARDATEFILTER = (
"""
<C:calendar-query xmlns:C="urn:ietf:params:xml:ns:caldav">
    <D:prop xmlns:D="DAV:">
        <D:getetag/>
    </D:prop>
    <C:filter>
        <C:comp-filter name="VCALENDAR">
            <C:comp-filter name="VEVENT">
                <C:time-range end="%s" start="%s"/>
            </C:comp-filter>
        </C:comp-filter>
    </C:filter>
</C:calendar-query>
"""
)

XML_REQ_CALENDARDATA = (
"""
   <C:calendar-multiget xmlns:C="urn:ietf:params:xml:ns:caldav">
    <D:prop xmlns:D="DAV:">
        <D:getetag/>
       <C:calendar-data>
         <C:comp name="VCALENDAR">
           <C:prop name="VERSION"/>
           <C:comp name="VEVENT">
             <C:prop name="SUMMARY"/>
             <C:prop name="UID"/>
             <C:prop name="DTSTART"/>
             <C:prop name="DTEND"/>
             <C:prop name="DURATION"/>
             <C:prop name="RRULE"/>
             <C:prop name="RDATE"/>
             <C:prop name="EXRULE"/>
             <C:prop name="EXDATE"/>
             <C:prop name="RECURRENCE-ID"/>
           </C:comp>
         </C:comp>
       </C:calendar-data>
    </D:prop>   
    %s
</C:calendar-multiget>
"""
)