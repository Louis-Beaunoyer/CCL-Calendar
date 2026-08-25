import datetime
from datetime import time

async def ainput(prompt_text="", allow_stop=False):
    window = __import__("js").window
    if "date" in prompt_text.lower() or "aaaa" in prompt_text.lower():
        value = await window.promptDateConsoleAsync(prompt_text, allow_stop)
        return str(value).replace("-", "/")
    return str(await window.promptUserConsoleAsync(prompt_text, allow_stop))

class Dayoff:
    def __init__(self,name,date):
        self.name = name
        self.date = date

class Breaks:
    def __init__(self, name, startDate, endDate):
        self.name = name
        self.startDate = startDate
        self.endDate = endDate

class Block:
    def __init__(self,name,startHour,endHour):
        self.name = name
        self.startHour = startHour
        self.endHour = endHour

class Day:
    def __init__(self,number,class1,class2,class3,class4):
        self.number = number
        self.class1 = class1
        self.class2 = class2
        self.class3 = class3
        self.class4 = class4

class Event:
    def __init__(self, name = None, dtstart = None, dtend = None, isAllDay: bool = False):
        self.name = name
        self.dtstart = dtstart
        self.dtend = dtend
        self.isAllDay = isAllDay


async def askForCycle()-> int:
    while True:
        cycle = int(await ainput('Cycle (1 ou 2): '))
        if cycle != 1 and cycle != 2:
            print('Veuillez entrer un cycle valide (1 ou 2)')
        else:
            return cycle

async def hour_selection():
    cycle1_start = [time(9,30), time(10,57), time(12,19), time(13,15), time(14,37), time(15,3)]
    cycle1_end = [time(10,52),time(12,19),time(13,15),time(14,37),time(15,3),time(16,25)]
    cycle1_friday_start = [time(9,30),time(10,19),time(11,8),time(11,52),time(12,32)]
    cycle1_friday_end = [time(10,14),time(11,3),time(11,52),time(12,32),time(13,16)]
    cycle2_start = [time(9,30),time(10,52),time(11,13),time(12,43),time(13,13),time(14,8),time(15,8)]
    cycle2_end = [time(10,52),time(11,13),time(12,35),time(13,13),time(14,8),time(15),time(16,30)]
    cycle2_friday_start = [time(9,30),time(10,19),time(11,3),time(11,43),time(12,32)]
    cycle2_friday_end = [time(10,14),time(11,3),time(11,43),time(12,27),time(13,16)]
    hours = []
    cycle = await askForCycle()
    if cycle == 1:

        hours.append(cycle1_start)
        hours.append(cycle1_end)
        hours.append(cycle1_friday_start)
        hours.append(cycle1_friday_end)
    else:
        hours.append(cycle2_start)
        hours.append(cycle2_end)
        hours.append(cycle2_friday_start)
        hours.append(cycle2_friday_end)
    return hours, cycle


async def day_classes():
    days_list = []
    async def ask_schedule(class_number,day):
        return await ainput(f'Quelle est la classe dans la plage horaire {class_number} le jour {day}?\n')

    for day in range(9):
        day = day + 1
        day_obj = Day(
            day,
            await ask_schedule(1, day),
            await ask_schedule(2, day),
            await ask_schedule(3, day),
            await ask_schedule(4, day),
        )
        days_list.append(day_obj)

    return days_list

async def askForInvertedDays():
    inverted_days = []
    i = 1
    while True:
        print('Pour arrêter de rentrer des dates, entrez "stop"')
        date = await ainput('Date (format: AAAA/MM/JJ): ', True)
        if date == 'stop':
            break
        date = date.replace('/', '')
        date = datetime.datetime.strptime(date, '%Y%m%d')
        dayNumber = await ainput('Jour: ', True)
        if dayNumber == 'stop':
            break
        i = i + 1
        inverted_days.append({'date': date, 'dayNumber': dayNumber})
    return inverted_days

async def askForBreaks():
    breaks_list = []
    while True:
        print('Pour arrêter d\'entrer des relâches, entrez "stop"')
        name = await ainput("Entrez le nom de la relâche: ", True)
        if name.lower() == 'stop':
            break
        start = await ainput('Entrez la date de debut de la relâche (format: AAAA/MM/JJ): ', True)
        if start.lower() == 'stop':
            break
        start = start.replace('/', '')
        start = datetime.date.strptime(start, '%Y%m%d')
        end = await ainput('Entrez la date de fin de la relâche (format: AAAA/MM/JJ): ', True)
        if end.lower() == 'stop':
            break
        end = end.replace('/', '')
        end = datetime.date.strptime(end, '%Y%m%d')
        b = Breaks(name, start, end)
        breaks_list.append(b)
    return breaks_list


async def askForDaysOff():
    days_off_list = []
    while True:
        print('Pour arrêter d\'entrer des congés, entrez "stop"')
        date = await ainput('Entrez la date de debut de la journée pédagogique (format: AAAA/MM/JJ): ', True)
        if date.lower() == 'stop':
            break
        else:
            date = date.replace('/', '')
            date = datetime.date.strptime(date, '%Y%m%d')

        while True:
            name = (await ainput("Entrez 'f' pour une journée flottante, 'c' pour un congé férié et 'p' pour une journée pédagogique: ")).lower()
            if name not in {'f', 'c', 'p'}:
                if name.lower() == 'stop': break 
                continue
            else:
                if name == 'f':
                    name = 'Journée flottante'
                elif name == 'c':
                    name = 'Congé férié'
                else:
                    name = 'Journée pédagogique'
                break

                day = Dayoff(name,date)
                days_off_list.append(day)
    return days_off_list

async def askForYearDateLimits():
    while True:
        start = await ainput('Entrez la date de debut de l\'année scolaire (format: AAAA/MM/JJ): ')
        start = start.replace('/', '')
        start = datetime.date.strptime(start, '%Y%m%d')
        end = await ainput('Entrez la date de fin de l\'année scolaire (format: AAAA/MM/JJ): ')
        end = end.replace('/', '')
        end = datetime.date.strptime(end, '%Y%m%d')
        return start, end

def isWeekend(date:datetime.date) -> bool:
    if date.weekday() in [5, 6]:
        return True
    else:
        return False

def isFriday(date:datetime.date) -> bool:
    if date.weekday() == 4:
        return True
    else:
        return False

