from calendar_utilities.utilities import *
import ics



yearDateLimits = askForYearDateLimits()
breaks:list = askForBreaks() #list of objects
daysOff:list = askForDaysOff() #list of objects
invertedDays:list[dict[datetime.date, int]] = askForInvertedDays() #list of dicts

hours, cycle = hour_selection() #list of lists
classesSchedule:list[object] = day_classes() #list of objects

daysInSchoolYear = abs((yearDateLimits[1] - yearDateLimits[0]).days+1)
eventList = []

i = 0
modifier = datetime.timedelta(days=0)
dayNumberIncrement = 1
while i <= daysInSchoolYear:
    currentDate = yearDateLimits[0] + datetime.timedelta(days=i) + modifier
    if dayNumberIncrement <= 10:
        dayNumberIncrement = 1

    if isWeekend(currentDate):
        continue


    breaksStartDays = [break_obj.startDate for break_obj in breaks]
    if currentDate in breaksStartDays:
        startDate = None
        endDate = None
        name = None
        isAllDay = True
        for break_obj in breaks:
            if currentDate == break_obj.startDate:
                name, startDate, endDate = break_obj.name, break_obj.startDate, break_obj.endDate
        event = Event(name, startDate, endDate, isAllDay)
        eventList.append(event)
        modifier = modifier + abs(endDate - startDate)
        continue


    daysOffDates = [day_off_obj.date for day_off_obj in daysOff]
    if currentDate in daysOffDates:
        startDate = None
        name = None
        isAllDay = True
        for day_off_obj in daysOff:
            if currentDate == day_off_obj.date:
                name, startDate= day_off_obj.name, day_off_obj.date
        event = Event(name, startDate, isAllDay)
        eventList.append(event)
        continue



    tempDayNumberIncrement = dayNumberIncrement

    invertedDaysKeys: list = [invertedDaysItem.keys() for invertedDaysItem in invertedDays]
    if currentDate in invertedDaysKeys:
        for invertedDaysItem in invertedDays:
            if currentDate == invertedDaysItem.keys():
                tempDayNumberIncrement = invertedDaysItem['dayNumber']



    if isFriday(currentDate):
        startTimes = hours[2]
        endTimes = hours[3]
    else:
        startTimes = hours[0]
        endTimes = hours[1]

    lunch = Event('Diner',startTimes[2],endTimes[2],False)
    dayNumber = Event(f'Jour {tempDayNumberIncrement}',currentDate,currentDate,True)
    class1 = Event(classesSchedule[tempDayNumberIncrement-1],startTimes[0],endTimes[0],False)
    class2 = Event(classesSchedule[tempDayNumberIncrement-1],startTimes[1],endTimes[1],False)
    if cycle == 1:
        class3 = Event(classesSchedule[tempDayNumberIncrement-1], startTimes[3], endTimes[3], False)
        class4 = Event(classesSchedule[tempDayNumberIncrement-1],startTimes[4],endTimes[4],False)
        eventList.extend([class1, class2,lunch, class3, class4])
    else:
        class3a = Event(classesSchedule[tempDayNumberIncrement - 1], startTimes[3], endTimes[3], False)
        class3b = Event(classesSchedule[tempDayNumberIncrement - 1], startTimes[4], endTimes[4], False)
        class4 = Event(classesSchedule[tempDayNumberIncrement - 1], startTimes[5], endTimes[5], False)
        eventList.extend([class1,class2,class3a,lunch, class3b, class4])




    dayNumberIncrement = dayNumberIncrement + 1
    i = i + 1

e = ics.Event()
c = ics.Calendar()
for event in eventList:
    e.name = event.name
    e.begin = event.dtstart
    e.end = event.dtend
    if event.isAllDay:
        e.make_all_day()
    c.events.add(e)

with open('calendar.ics', 'w') as file:
    file.writelines(c.serialize())

