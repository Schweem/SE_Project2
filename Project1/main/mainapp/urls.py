from django.urls import path
from . import views

urlpatterns = [
        path('todo/', views.todo_list, name='todo_list'),
        path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
        path('mark_completed/<int:todo_id>/', views.mark_todo_completed, name='mark_todo_completed'),
        path('calendar/<str:period>/', views.calendar_view, name='calendar'),
        path('event/<int:event_id>/', views.event_detail, name='event_detail'),

        path('reading-list/', views.reading_material_view, name='reading-list'),
        path('class_list/', views.class_list_view, name='class_list'),
        path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),
        path('hours/', views.hours, name='hours'),
        path('timer/', views.pomodoro_timer, name='timer'),
        path('draw/', views.draw_view, name='draw'), 
        path('memes/', views.memes, name='memes'),
        path('', views.home, name='home')
        
]