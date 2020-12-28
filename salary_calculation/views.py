from django.shortcuts import render
from django.forms import formset_factory

from .forms import HourForm, CalculateForm, TotalForm

from datetime import datetime, date, time, timedelta

from .utils import create_fortnight, check_hour_type, sum_hours_type


def salary(request):

    hour_form = HourForm()

    if request.method == 'POST':

        return render(request, 'salary_calculation/hours.html')

    return render(request, 'salary_calculation/salary.html', {'hour_form':hour_form})
    

def hours(request):

    year = int(request.POST.get('start_date_year'))
    month = int(request.POST.get('start_date_month'))
    day = int(request.POST.get('start_date_day'))
    salary_month = float(request.POST.get('salary_month'))
    request.session['salary_month'] = salary_month

    start_date = datetime(year, month, day)
    fortnight = create_fortnight(start_date)

    initial_formset = [{'day':fortnight[i], 'start_hour':6, 'hour_number':8} for i in range(len(fortnight))]
    CalculateFormSet = formset_factory(CalculateForm, extra=0)
    formset = CalculateFormSet(initial=initial_formset)

    return render(request, 'salary_calculation/hours.html', {'formset':formset})

    # if request.method == 'POST':
    #     salary_month = float(request.GET.get('salary', 0))
    #     salary_fortnight = salary_month / 2
    #     salary_day = salary_month / 30
    #     salary_hour = salary_month / 240

    #     total_hours_cost = HOURS_EMPTY
    #     sum_hours = HOURS_EMPTY
    #     total_extra_hours = 0

    #     formset = CalculateFormSet(request.POST, initial=initial)

    #     forms_number = int(request.POST.get('form-TOTAL_FORMS', 0))
    #     list_forms_number = [str(i) for i in range(forms_number)]
       
    # #     if hour_form.is_valid():
            
    # #         year = int(request.POST['start_date_year'])
    # #         month = int(request.POST['start_date_month'])
    # #         day = int(request.POST['start_date_day'])
    # #         start_date = datetime(year, month, day)

    # #         fortnight = create_fortnight(start_date)

    # #         initial = [{'day':fortnight[i], 'start_hour':22, 'hour_number':8} for i in range(len(fortnight))]

    # #         CalculateFormSet = formset_factory(CalculateForm, extra=0)
    # #         formset = CalculateFormSet(initial=initial)

    # #         note = 'This is your salary'
    # #     else:
    # #         note = "Error"
    # #     return render(request, 'salary_calculation/salary.html', 
    # #         {'note': note, 'hour_form': hour_form, 'formset':formset})
    # # else:
    # #     hour_form = HourForm()
    # #     return render(request, 'salary_calculation/salary.html', 
    # #                 {'hour_form': hour_form, 'formset':formset})


def total(request):

    print(request.POST)

    HOURS_COST = {'ordinaria':1, 'extra_diurna':1.25, 'recargo_nocturno':1.35, 
        'extra_nocturna':1.75, 'dominical_diurna':1.75, 
        'extra_dominical_diurna':2.0, 'dominical_nocturna':2.1,
        'extra_dominical_nocturna':2.5}

    sum_hours_total = {'ordinaria':0.0, 'extra_diurna':0.0, 'recargo_nocturno':0.0, 
        'extra_nocturna':0.0, 'dominical_diurna':0.0, 
        'extra_dominical_diurna':0.0, 'dominical_nocturna':0.0,
        'extra_dominical_nocturna':0.0}

    total_hours_cost = {'ordinaria':0.0, 'extra_diurna':0.0, 'recargo_nocturno':0.0, 
        'extra_nocturna':0.0, 'dominical_diurna':0.0, 
        'extra_dominical_diurna':0.0, 'dominical_nocturna':0.0,
        'extra_dominical_nocturna':0.0}

    total_extra_hours = 0
    total_ordinaria_hours = 0

    forms_number = int(request.POST.get('form-TOTAL_FORMS', 0))
    list_forms_number = [str(i) for i in range(forms_number)]
    
    for i in list_forms_number:

        year = request.POST['form-'+i+'-day_year']
        month = request.POST['form-'+i+'-day_month']
        day = request.POST['form-'+i+'-day_day']

        start_hour = request.POST['form-'+i+'-start_hour']

        start_date = datetime(int(year), int(month), int(day), int(start_hour))

        hour_number = int(request.POST['form-'+i+'-hour_number'])

        hours_list = [start_date + timedelta(hours=i) for i in range(hour_number)]
        hours_dict = {i+1:hours_list[i] for i in range(hour_number)}

        hours_type_dict = check_hour_type(hours_dict)

        sum_hours = sum_hours_type(hours_type_dict)

        for key in sum_hours_total:
            sum_hours_total[key] += sum_hours[key]

    print('sum hours total:', sum_hours_total)

    for key in sum_hours_total:
        if key == 'ordinaria':
            total_ordinaria_hours += sum_hours_total[key]
    
    for key in total_hours_cost:
        total_hours_cost[key] += HOURS_COST[key] * sum_hours_total[key]

    print('total_hours_cost:', total_hours_cost)

    for key in total_hours_cost:
        if key != 'ordinaria':
            total_extra_hours += total_hours_cost[key]
        
    print('Total extra hours:', total_extra_hours)
    
    
    salary_month = request.session['salary_month']
    print(salary_month)
    salary_fortnight = salary_month / 2
    salary_day = salary_month / 30
    salary_hour = salary_month / 240
    
    salud = salary_fortnight * 0.04
    pension = salary_fortnight * 0.04
    salud_y_pension = salud + pension

    auxilio_transporte_month = 102854
    auxilio_transporte_fortnight = auxilio_transporte_month / 2
    auxilio_transporte_day = auxilio_transporte_month / 30

    # print(len(list_forms_number))
    print('Total extra hours:', total_extra_hours)

    if len(list_forms_number) < 16:

        salary_total = round(total_extra_hours * salary_hour + 
                            salary_hour * total_ordinaria_hours + 
                            auxilio_transporte_fortnight
                             - salud_y_pension)

    else:
        salary_total = round(total_extra_hours * salary_hour + 
                            salary_hour * total_ordinaria_hours + 
                            auxilio_transporte_fortnight
                             + salary_day + auxilio_transporte_day 
                             - salud_y_pension)

    print('SALARY: ', round(salary_total))
    
    return render(request, 'salary_calculation/total.html', {'salary_total':salary_total})