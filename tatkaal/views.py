from django.shortcuts import render, redirect
from .models import Train, Ticket, Wallet
from django.http import HttpResponse
from django.forms.models import model_to_dict

# Create your views here.

def index(reqeust):
    trains = list(Train.objects.all())
    return render(reqeust, 'tatkaal/index.html', {'trains': trains})

def book(request, train_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    train = Train.objects.get(id=train_id)
    available_seats = train.total_seats - len(list(Ticket.objects.filter(train=train)))
    if available_seats <= 0:
        return HttpResponse(f"Not enough seats in train.\n {available_seats} seats available")
    return render(request, 'tatkaal/book.html', {'train': train, 'seats_available': available_seats})

def book_confirm(request, train_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        train = Train.objects.get(id=train_id)
        seats_booked = len(list(Ticket.objects.filter(train=train)))
        if seats_booked >= train.total_seats:
            return HttpResponse(f"Not enough seats in train.\n + {str(train.seats-seats_booked)} seats available")
        passengers = dict(request.POST)
        passengers.pop('csrfmiddlewaretoken')
        tickets_booked = []
        try:
            wallet = Wallet.objects.filter(user=request.user)[0]
        except IndexError:
            wallet = Wallet(user=request.user, balance=0)
            wallet.save()
            redirect('/add_money')

        for passenger in passengers:
            ticket = Ticket(train=train, user=request.user, passenger_name=passengers[passenger][0], seat_no=seats_booked+1)
            seats_booked += 1
            ticket.save()
            wallet.balance -= train.gen_price
            tickets_booked.append([ticket.__dict__["passenger_name"], ticket.__dict__["seat_no"]])

        wallet.save()
        print(tickets_booked)
        print(wallet.__dict__)

        content = '<a href="/">Home</a> <br>'
 
        for ticket in tickets_booked:
            content += f"Passenger Name: {ticket[0]}, Seat No: {ticket[1]} <br>"

        return HttpResponse("Booked <br>" + content + "<br> <a href='/'>Go back</a>")

    return redirect('')

def add_money(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        try:
            wallet = Wallet.objects.filter(user=request.user)[0]
        except IndexError:
            wallet = Wallet(user=request.user, balance=0)
            wallet.save()
            redirect('/add_money')

        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')
        wallet.balance += int(data['amount'][0])
        wallet.save()
        return HttpResponse("Added " + data['amount'][0] + " to your wallet")

    return render(request, 'tatkaal/add_money.html')


def view_tickets(request):
    if not request.user.is_authenticated:
        return redirect('')

    # get all tickets from currentuser 
    tickets = list(Ticket.objects.all().filter(user=request.user))
    tickets = [model_to_dict(ticket) for ticket in tickets]

    try:
        trains = Train.objects.all().filter(id=tickets[0]['train'])
    except IndexError:
        return HttpResponse("No tickets booked yet <a href='/'>Go back</a>")
    train_data = {}
    for train in trains:
        train_data[train.id] = model_to_dict(train)

    print(tickets)
    print(train_data)
    return render(request, 'tatkaal/view_tickets.html', {'tickets': tickets, 'trains': train_data})


def view_ticket(request, ticket_id):
    if not request.user.is_authenticated:
        return redirect('')

    ticket = Ticket.objects.get(id=ticket_id)
    train = Train.objects.get(id=ticket.train.id)
    return render(request, 'tatkaal/view_ticket.html', {'ticket': model_to_dict(ticket), 'train': model_to_dict(train)})


def cancel_ticket(request, ticket_id):
    if not request.user.is_authenticated:
        return redirect('')

    ticket = Ticket.objects.get(id=ticket_id)
    ticket.delete()

    return HttpResponse("Ticket cancelled successfully <br> <a href='/view_tickets'>Go back</a>")