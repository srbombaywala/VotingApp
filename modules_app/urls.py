from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.index, name="index" ),
    path('register/', view=views.register, name="register"),
    path('generateOTP/', view=views.generateOTP, name="generateOTP"),
    path('logintovote/', view=views.logintovote, name="logintovote"),
    path('popup_modal/<int:voter_id>/', views.popup_modal, name='popup_modal'),
    path('member_list_popup/', views.member_list_popup, name='member_list_popup'),
    path('result/', views.candidate_votes, name='candidate_votes'),
    path('user_search/', views.user_search, name="user_search"),
    path('voted/', views.voted, name="voted"),

]
