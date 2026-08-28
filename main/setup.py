from calendar_utilities.utilities import *
import ics
from zoneinfo import ZoneInfo as tmz


yearDateLimits = await askForYearDateLimits()
breaks:list = await askForBreaks() #list of objects
daysOff:list = await askForDaysOff() #list of objects
invertedDays:list[dict[datetime.date, int]] = await askForInvertedDays() #list of dicts

hours, cycle = await hour_selection() #list of lists
classesSchedule:list[object] = await day_classes() #list of objects

daysInSchoolYear = abs((yearDateLimits[1] - yearDateLimits[0]).days+1)
eventList = []

i = 0
dayNumberIncrement = 1
while i < daysInSchoolYear:
    currentDate = yearDateLimits[0] + datetime.timedelta(days=i)
    if dayNumberIncrement > len(classesSchedule):
        dayNumberIncrement = 1

    if isWeekend(currentDate):
        i = i + 1
        continue

    for break_obj in breaks:
        if break_obj.endDate > yearDateLimits[1]:
            break_obj.endDate = yearDateLimits[1]

    breaksStartDays = [break_obj.startDate for break_obj in breaks]
    if currentDate in breaksStartDays:
        startDate = None
        endDate = None
        name = None
        for break_obj in breaks:
            if currentDate == break_obj.startDate:
                name, startDate, endDate = break_obj.name, break_obj.startDate, break_obj.endDate
        event = Event(
            name,
            datetime.datetime.combine(startDate, datetime.time()),
            datetime.datetime.combine(endDate, datetime.time()),
            True,
        )
        eventList.append(event)
        i = i + 1 + (endDate - startDate).days
        continue


    daysOffDates = [day_off_obj.date for day_off_obj in daysOff]
    if currentDate in daysOffDates:
        startDate = None
        name = None
        for day_off_obj in daysOff:
            if currentDate == day_off_obj.date:
                name, startDate= day_off_obj.name, day_off_obj.date
        event = Event(
            name,
            datetime.datetime.combine(startDate, datetime.time()),
            datetime.datetime.combine(startDate, datetime.time()),
            True,
        )
        eventList.append(event)
        i = i +1
        continue



    tempDayNumberIncrement = dayNumberIncrement

    for invertedDaysItem in invertedDays:
        if currentDate == invertedDaysItem['date'].date():
            tempDayNumberIncrement = int(invertedDaysItem["dayNumber"])




    if isFriday(currentDate):
        startTimes = hours[2]
        endTimes = hours[3]
    else:
        startTimes = hours[0]
        endTimes = hours[1]

    startTimes = [
        datetime.datetime.combine(currentDate, hour)
        for hour in startTimes
    ]
    endTimes = [
        datetime.datetime.combine(currentDate, hour)
        for hour in endTimes
    ]

    currentDateTime = datetime.datetime.combine(currentDate, datetime.time())
    dayNumber = Event(
        f'Jour {tempDayNumberIncrement}',
        currentDateTime,
        currentDateTime,
        True,
    )
    class1 = Event(classesSchedule[tempDayNumberIncrement-1].class1,startTimes[0],endTimes[0],False)

    if cycle == 1:
        class2 = Event(classesSchedule[tempDayNumberIncrement-1].class2,startTimes[1],endTimes[1],False)

        if isFriday(currentDate):
            lunch = Event('Diner',startTimes[3],endTimes[3],False)
            class3 = Event(classesSchedule[tempDayNumberIncrement - 1].class3, startTimes[2], endTimes[2], False)
            class4 = Event(classesSchedule[tempDayNumberIncrement-1].class4,startTimes[4],endTimes[4],False)
        else:
            lunch = Event('Diner', startTimes[2], endTimes[2], False)
            class3 = Event(classesSchedule[tempDayNumberIncrement-1].class3, startTimes[3], endTimes[3], False)
            class4 = Event(classesSchedule[tempDayNumberIncrement - 1].class4, startTimes[4], endTimes[4], False)
        eventList.extend([class1, class2,lunch, class3, class4])
    else:

        if isFriday(currentDate):
            lunch = Event('Diner',startTimes[2],endTimes[2],False)
            class2 = Event(classesSchedule[tempDayNumberIncrement - 1].class2, startTimes[1], endTimes[1], False)
            class3 = Event(classesSchedule[tempDayNumberIncrement - 1].class3, startTimes[3], endTimes[3], False)
            class4 = Event(classesSchedule[tempDayNumberIncrement-1].class4,startTimes[4],endTimes[4],False)
            eventList.extend([class1, class2, lunch, class3, class4])
        else:
            lunch = Event('Diner', startTimes[3], endTimes[3], False)
            class2 = Event(classesSchedule[tempDayNumberIncrement - 1].class2, startTimes[1], endTimes[1], False)
            class3a = Event(classesSchedule[tempDayNumberIncrement-1].class3, startTimes[2], endTimes[2], False)
            class3b = Event(classesSchedule[tempDayNumberIncrement - 1].class3, startTimes[4], endTimes[4], False)
            class4 = Event(classesSchedule[tempDayNumberIncrement - 1].class4, startTimes[5], endTimes[5], False)
            eventList.extend([class1, class2, class3a, lunch, class3b, class4])

    eventList.append(dayNumber)




    dayNumberIncrement = dayNumberIncrement + 1
    i = i + 1

timezone = tmz("America/Toronto")
c = ics.Calendar()
for event in eventList:
    e = ics.Event()
    e.name = event.name
    if event.isAllDay:
        e.begin = event.dtstart
        e.end = event.dtend
        e.make_all_day()
    else:
        e.begin = event.dtstart.replace(tzinfo=timezone)
        e.end = event.dtend.replace(tzinfo=timezone)
    c.events.add(e)

calendar_data = c.serialize()
with open('calendar.ics', 'w') as file:
    file.write(calendar_data)

window = __import__("js").window
window.downloadFile("calendar.ics", calendar_data, "text/calendar")
