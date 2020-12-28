from datetime import datetime, timedelta, date

from .constants import Holyday, Constant

def is_holyday_or_sunday(given_date):

    date = datetime(given_date.year, given_date.month, given_date.day)

    if date.weekday() == 6 or Holyday().is_holyday(date):
        return True
    return False

def create_fortnight(given_date):
    ''' given date is a datetime field
    return fornight as a list of date fields
    '''
    day = given_date.day
    month = given_date.month
    year = given_date.year

    given_date = date(year, month, day)

    fortnight = [given_date + timedelta(days=i) for i in range(16)]

    fortnight = [date for date in fortnight if date.month == month]

    if day <= 15:
        fortnight = [date for date in fortnight if date.day <= 15]

    return fortnight

def check_hour_type(hours_dict):

    type_hours_dict = {}

    for key, value in hours_dict.items():

        hour = value.hour
        holyday_or_sunday = is_holyday_or_sunday(value)

        if key <= 8:

            if hour not in Constant.night_hours and not holyday_or_sunday:
                hour_type = 'ordinaria'
            if hour in Constant.night_hours and not holyday_or_sunday:
                hour_type = 'recargo_nocturno'
            if hour in Constant.night_hours and holyday_or_sunday:
                hour_type = 'dominical_nocturna'
            if holyday_or_sunday and hour not in Constant.night_hours:
                hour_type = 'dominical_diurna'
        else:
            if hour not in Constant.night_hours and not holyday_or_sunday:
                hour_type = 'extra_diurna'
            if hour in Constant.night_hours and not holyday_or_sunday:
                hour_type = 'extra_nocturna'
            if hour in Constant.night_hours and holyday_or_sunday:
                hour_type = 'extra_dominical_nocturna'
            if holyday_or_sunday and hour not in Constant.night_hours:
                hour_type = 'extra_dominical_diurna'

        type_hours_dict[key] = hour_type

    return type_hours_dict

def sum_hours_type(hours_type_dict):

    sum_hours = {'ordinaria':0.0, 'extra_diurna':0.0, 'recargo_nocturno':0.0, 
        'extra_nocturna':0.0, 'dominical_diurna':0.0, 
        'extra_dominical_diurna':0.0, 'dominical_nocturna':0.0,
        'extra_dominical_nocturna':0.0}

    for value in hours_type_dict.values():
        sum_hours[value] += 1

    return sum_hours