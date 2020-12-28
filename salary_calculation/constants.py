from datetime import datetime

class Holyday:
    days = [datetime(2020, 12, 8), datetime(2020, 12, 25),
            datetime(2021, 1, 1), datetime(2021, 1, 11),
            datetime(2021, 3, 22), datetime(2021, 4, 1),
            datetime(2021, 4, 2), datetime(2021, 5, 1),
            datetime(2021, 5, 17), datetime(2021, 6, 7),
            datetime(2021, 6, 14), datetime(2021, 7, 5),
            datetime(2021, 7, 20), datetime(2021, 8, 7),
            datetime(2021, 8, 16), datetime(2021, 10, 18),
            datetime(2021, 11, 1), datetime(2021, 11, 15),
            datetime(2021, 12, 8), datetime(2021, 12, 25),
    ]

    def __init__(self):
        pass

    def is_holyday(self, date):

        return date in Holyday.days

class Constant:
    night_hours = [21, 22, 23, 0, 1, 2, 3, 4, 5]
