import itertools
import datetime
import numpy as np
from extraction_baseclass import tryPath

def fixUnknownDate(date,month,day):
    if len(date) == 4:
        date += "-" + month
    if len(date) == 7:
        date += "-" + day
    return date

def updateResource(res, path, new_value):
    obj_ptr = res
    for key in path:
        if key == path[-1]:
            obj_ptr[key] = new_value
        obj_ptr = obj_ptr[key]

def fixDates(dateList):
    date2fixedDate = {}
    for date in dateList:
        date2fixedDate[date] = datetime.datetime.strptime(fixUnknownDate(date[:10],"01","01"), "%Y-%m-%d")
    return date2fixedDate

class dateChanger:

    def __init__(self, dateFields = [['effectivePeriod','start'],['effectivePeriod','end'],['effectiveDateTime']]):
        self.dateFields = dateFields
    
    def addDateField(self, dateField):
        self.dateFields.append(dateField)
    
    def collectDatesFromResource(self, resource):
        res = [tryPath(resource, x) for x in self.dateFields]
        res = [x for x in res if x is not None]
        return res
    
    def collectDates(self, resources):
        dateList = [self.collectDatesFromResource(x) for x in resources]
        dateList = list(itertools.chain.from_iterable(dateList))
        dateList = list(set(dateList))
        return dateList

    def addRandomNoise(self, resources, changeMin = -10, changeMax = 11, seed = None):
        rng = np.random.default_rng(seed = seed)
        deltaGlobal = datetime.timedelta(days=int(rng.integers(-400,401)))
        date2fixedDate = fixDates(self.collectDates(resources))
        allDates = list(set(date2fixedDate.values()))
        allDates.sort()
        shiftedDates = [x + deltaGlobal + datetime.timedelta(days=int(rng.integers(changeMin,changeMax))) for x in allDates]
        shiftedDates.sort()
        
        fixedDate2shiftedDate = {allDates[i]: shiftedDates[i] for i in range(len(allDates))}
        
        # now change resources:
        for res in resources:
            for dateField in self.dateFields:
                if value := tryPath(res, dateField):
                    updateResource(res, dateField, fixedDate2shiftedDate[date2fixedDate[value]].strftime('%Y-%m-%d'))