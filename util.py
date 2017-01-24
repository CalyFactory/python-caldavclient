import requests
from urllib.parse import urlparse

def requestData(method = "PROPFIND", hostname = "", depth = 0, data = "", auth = ("","")):
    response = requests.request(
        method,
        hostname,
        data = data, 
        headers = {
            "Depth" : str(depth)
        },
        auth = auth 
    )

    if response.status_code<200 or response.status_code>299:
        raise Exception('http code error' + str(response.status_code))

    return response

def getHostnameFromUrl(url):
    parsedUrl = urlparse(url)
    hostname = '{uri.scheme}://{uri.netloc}'.format(uri=parsedUrl)
    return hostname


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def calListToDict(calendarList):
    calDict = {}
    for calendar in calendarList:
        calDict[calendar.calendarUrl] = calendar.cTag
    return calDict

def eventListToDict(eventList):
    eventDict = {}
    for event in eventList:
        eventDict[event.eventUrl] = event.eTag

def findCalendar(key, list):
    for calendar in list:
        if calendar.calendarUrl == key:
            return calendar

def diffCalendar(oldList, newList):
    diffList = []
    for calendar in oldList:
        newCalendar = findCalendar(calendar.calendarUrl, newList)
        if newCalendar.cTag != calendar.cTag:
            diffList.append([calendar, newCalendar])
    return diffList

def diffEvent(oldList, newList):
    return DictDiffer(
        eventListToDict(oldList), 
        eventListToDict(newList)
    )