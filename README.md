Скрипт создания google-календаря с днями рождений и возможностью добавлять
уведомления о днях рождения.

1. Перейти к [google календарю](https://calendar.google.com/calendar/u/0/r)
2. Открыть настройки:
    -  (Шестерёнка справа вверху)
    - Настройки
3. Экспортировать все календари:
    - Слева "Импорт и экспорт"
    - "Экспорт"
4. Распаковать календарь "Contacts" в "./data/". Имя файла задаётся в классе Paths
5. Запустить текущий скрипт
6. Создать в Google Calendar новый календарь, например "Уведомления дни рождения":
    - Слева "Добавить календарь"
    - "Создать календарь"
7. Добавить в созданный календарь события из файла:
    - Слева "Импорт и экспорт"
    - "Импорт"
    - Выбрать календарь "Уведомления дни рождения"
    - Импортировать события из созданного файла
8. Включить уведомления:
    - Слева "Настройки моих календарей"
    - "Уведомления дни рождения"
    - "Мероприятия на весь день"
    - За 0 дней в 10:00
