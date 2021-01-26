from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.core.mail import send_mail, BadHeaderError

from .forms import ContactForm

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings

# def home(request):

#     if request.method == 'GET':
#         form = ContactForm()
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             subject = form.cleaned_data['subject']
#             sender = form.cleaned_data['sender']
#             message = form.cleaned_data['message']
#             full_message = "from: {}\n{}\nsubject: {}\n{}".format(name, sender, subject, message)
#             try:
#                 send_mail(subject, full_message, 'acalvm@gmail.com', ['acalvm@gmail.com'], fail_silently=True)
#             except BadHeaderError:
#                 return HttpResponse("Invalid header found.")
#             return redirect('sucess')

#     return render(request, 'home/portfolio.html', {'form': form})


def home(request):

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']

            message = Mail(
                from_email='acamilo.alvarez@udea.edu.co',
                to_emails='acalvm@gmail.com',
                subject=subject,
                html_content='''<strong>Name: </strong>{}<br>
                                <strong>Email: </strong>{}<br>
                                <strong>Message: </strong>{}'''.format(name, sender, message)
            )

            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            return redirect('sucess')

    return render(request, 'home/index.html', {'form': form})

def successView(request):

    return render(request, 'home/successView.html')
