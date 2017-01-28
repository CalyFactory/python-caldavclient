
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