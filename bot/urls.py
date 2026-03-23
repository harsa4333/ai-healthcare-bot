# bot/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('', views.home_view, name='home'),
    path('chat/', views.chat_view, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('clear-chat/', views.clear_chat, name='clear_chat'),
    path('chat-history/', views.chat_history_view, name='chat_history'),
    path('find-doctors/', views.find_doctors, name='find_doctors'),
    path('find-hospitals/', views.find_hospitals, name='find_hospitals'),
]