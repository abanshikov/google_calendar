#!./venv/bin/python
import os
import datetime
import uuid
import logging
from dataclasses import dataclass
from pathlib import Path
from icalendar import Calendar, Event


logging.basicConfig(
    format=u'%(levelname)s:\t'
           u'[%(filename)s] '
           u'[LINE:%(lineno)s] '
           u'[%(asctime)s]: '
           u'%(message)s',
    datefmt='%H:%M',
    level=logging.DEBUG,
)


@dataclass(frozen=True)
class Paths:
    """Настройки путей каталогов и файлов."""
    sep: str = os.path.sep
    current_file: str = os.path.abspath(__file__)
    current_path: str = sep.join(current_file.split(sep)[:-1])
    project: str = str(Path(current_path)) + sep
    data: str = str(Path().joinpath(project, "data")) + sep
    addressbook_calendar: str = f"{data}addressbook#contacts@group.v.calendar.google.com.ics"
    output_calendar: str = f"{data}birthday_notifications.ics"


@dataclass(frozen=True)
class AttributeNames:
    """Названия атрибутов данных."""
    dtstart: str = "DTSTART"
    dtend: str = "DTEND"
    rrule: str = "RRULE"
    dtstamp: str = "DTSTAMP"
    uid: str = "UID"
    created: str = "CREATED"
    description: str = "DESCRIPTION"
    last_modified: str = "LAST-MODIFIED"
    sequence: str = "SEQUENCE"
    status: str = "STATUS"
    summary: str = "SUMMARY"
    transp: str = "TRANSP"


@dataclass
class Data:
    """Полученные данные"""
    dtstart: str = ""
    dtend: str = ""
    rrule: str = ""
    dtstamp: str = ""
    uid: str = ""
    created: str = ""
    description: str = ""
    last_modified: str = ""
    sequence: str = ""
    status: str = ""
    summary: str = ""
    transp: str = ""


class MyCalendar:
    """Работа с календарями"""
    def __init__(self) -> None:
        self.data: list = []
        self.cache: list = []

    def get_data(self) -> None:
        """Получение данных из календаря контактов"""
        try:
            g = open(Paths.addressbook_calendar, 'rb')
        except Exception:
            logging.error('Не верно указано название файла календаря контактов:\n' + Paths.addressbook_calendar)
            return
        logging.info("Получение событий из файла календаря.")
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk()[:]:
            data = Data()
            current_time = datetime.datetime.now()
            if component.name == "VEVENT":
                if str(component.get("summary")) in self.cache:
                    continue
                data.dtstart = component.get('DTSTART').dt
                data.dtend = component.get("DTEND").dt
                data.rrule = {'freq': 'yearly'}
                data.dtstamp = current_time
                data.uid = str(uuid.uuid4().hex) + "@google.com"
                data.created = current_time
                data.description = str(component.get("UID"))
                data.last_modified = current_time
                data.sequence = str(component.get("sequence"))
                data.status = str(component.get("status"))
                data.summary = str(component.get("summary"))
                data.transp = str(component.get("transp"))
                self.cache.append(str(component.get("summary")))
            else:
                continue
            self.data.append(data)
        g.close()
        logging.info(f"Количество созданных событий: {len(self.data)}")

    def create(self) -> None:
        """Создание собственного календаря"""
        cal = Calendar()
        cal.add('prodid', '-//Birthday calendar//')
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('x-wr-calname', 'Birthday Notifications')
        cal.add('x-wr-timezone', 'UTC')

        attrs = AttributeNames()
        for data in self.data:
            persone_data = {}
            for item in attrs.__dict__:
                persone_data[attrs.__getattribute__(item)] = data.__getattribute__(item)
            event = Event()
            for key, value in persone_data.items():
                event.add(key, value)
            cal.add_component(event)
        f = open(Paths.output_calendar, 'wb')
        f.write(cal.to_ical())
        f.close()
        logging.info(f"Данные записаны в файл:\n{Paths.output_calendar}")


def main():
    my_calendar = MyCalendar()
    my_calendar.get_data()
    my_calendar.create()


if __name__ == "__main__":
    main()
