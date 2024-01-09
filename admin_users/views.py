from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from tatkaal.models import Train, Ticket
from django.http import HttpResponse, FileResponse
import mimetypes
import xlsxwriter
import io

# Create your views here.

# make sure all views are restricted to admin access
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#the-login-required-decorator

def dashboard(request):
    if not request.user.is_superuser:
        return redirect('/')

    trains = list(Train.objects.all())
    trains = {'trains': [model_to_dict(train) for train in trains]}
    return render(request, 'admin_users/dashboard.html', trains)

def add_train(request):
    if not request.user.is_superuser:
        return redirect('')
    
    if request.method == 'POST':
        data = dict(request.POST.copy())
        train = Train()
        data['id'] = [int(data['id'][0])]
        data['total_seats'] = [int(data['total_seats'][0])]
        data['duration'] = [int(data['duration'][0])]
        data['gen_price'] = [int(data['gen_price'][0])]
        for key in data:
            if key == 'csrfmiddlewaretoken':
                continue
            setattr(train, key, data[key][0])
        train.save()
        return redirect('/admin_dashboard')

    return render(request, 'admin_users/add_train.html')

def add_station(request):
    if not request.user.is_superuser:
        return redirect('')

    return render(request, 'admin_users/add_station.html')

def edit_train(request, train_id):
    if not request.user.is_superuser:
        return redirect('')

    train = Train.objects.get(id=train_id)
    
    if request.method == 'POST':
        data = dict(request.POST.copy())
        data['id'] = [int(data['id'][0])]
        data['total_seats'] = [int(data['total_seats'][0])]
        data['duration'] = [int(data['duration'][0])]
        data['gen_price'] = [int(data['gen_price'][0])]
        for key in data:
            if key == 'csrfmiddlewaretoken':
                continue
            setattr(train, key, data[key][0])
        train.save()
        return redirect('/admin_dashboard')
    
    return render(request, 'admin_users/edit_train.html', {'train': model_to_dict(train)})
    
def delete_train(request, train_id):
    if not request.user.is_superuser:
        return redirect('')

    train = Train.objects.get(id=train_id)
    train.delete()
    return HttpResponse("Deleted train " + str(train_id) + " successfully\n <a href='/admin_dashboard'>Go back</a>")

def check_bookings(request, train_id):
    if not request.user.is_superuser:
        return redirect('')

    tickets = list(Ticket.objects.all().filter(train=train_id))
    tickets = [model_to_dict(ticket) for ticket in tickets]
    return render(request, 'admin_users/check_bookings.html', {'tickets': tickets})

def export_to_excel(request, train_id):
    if not request.user.is_superuser:
        return redirect('')

    tickets = list(Ticket.objects.all().filter(train=train_id))
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()

    for u, field in enumerate(model_to_dict(tickets[0])):
        worksheet.write(f'{alpha[u]}1', field)

    for i, ticket in enumerate(tickets):
        t = model_to_dict(ticket)
        for j, field in enumerate(t):
            worksheet.write(f'{alpha[j]}{i+2}', t[field])

    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='report.xlsx')
