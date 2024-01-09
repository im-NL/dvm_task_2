# make admins redirect to this app's urls

from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('add_train', views.add_train, name='add_train'),
    path('edit_train/<int:train_id>/', views.edit_train, name='edit_train'),
    path('delete_train/<int:train_id>/', views.delete_train, name='delete_train'),
    path('check_bookings/<int:train_id>/', views.check_bookings),
    path('export_to_excel/<int:train_id>/', views.export_to_excel, name='export_to_excel'),
    # path('add_station/', views.add_station, name='add_station'),
    # path('add_route/', views.add_route, name='add_route'),
]
