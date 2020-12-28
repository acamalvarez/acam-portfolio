from django import forms

import datetime

months = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril',
        5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto',
        9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}

class HourForm(forms.Form):
    salary_month = forms.IntegerField(initial= 877803, 
                                max_value=100000000, 
                                min_value=0, label='Salario')
    start_date = forms.DateField(initial=datetime.date.today, 
                                label='Fecha de inicio', 
                                widget=forms.SelectDateWidget(months=months))

class CalculateForm(forms.Form):
    day = forms.DateField(widget=forms.SelectDateWidget(months=months))
    start_hour = forms.IntegerField(min_value=0, max_value=23, 
                                widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
    hour_number = forms.IntegerField(min_value=0, max_value=12, 
                                widget=forms.NumberInput(attrs={'style': 'width: 50px'}))

class TotalForm(forms.Form):
    total = forms.CharField(max_length=100)
