from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
     path('login/',views.login,name='login'),
      path('register/',views.register,name='register'),
      path('about/',views.about,name='about'),
      path('contact/',views.contact,name='contact'),
      path('jobs/',views.jobs,name='jobs'),
      path('jobdetails/<id>',views.jobdetails,name='jobdetails'),
       path('forgot-password/', views.forgot_password, name='forgot_password'),
       path('savedjob/<id>', views.savedjob, name='savedjob'),
      
]