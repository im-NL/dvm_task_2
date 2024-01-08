from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("book/<int:train_id>/", views.book),
    path("book/<int:train_id>/confirm/", views.book_confirm),
    path("add_money/", views.add_money),
    path('view_tickets/', views.view_tickets, name='view_tickets'),
    path('view_tickets/<int:ticket_id>/', views.view_ticket, name='view_ticket'),
    path('cancel_ticket/<int:ticket_id>/', views.cancel_ticket, name='cancel_ticket'),
]
