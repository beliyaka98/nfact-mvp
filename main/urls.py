from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainPage , name='main'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path('friends/', views.friends, name='friends'),
    path('createrelationship/<profile_id>/', views.create_relationship, name='create_relationship'),
    path('acceptrelationship/<profile_id>/', views.accept_relationship, name='accept_relationship'),
    path('declinerelationship/<profile_id>/', views.decline_relationship, name='decline_relationship'),
    path('acceptchallengerelationship/<profile_id>/', views.accept_challenge_relationship, name='accept_challenge_relationship'),
    path('declinechallengerelationship/<profile_id>/', views.decline_challenge_relationship, name='decline_challenge_relationship'),
    path('profile/', views.profilePage, name='profile'),
    path('challenges/', views.challenges, name='challenges'),
]
