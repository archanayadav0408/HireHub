from django.urls import path
from . import views



urlpatterns = [
    path('jobseekerdash/',views.jobseekerdash,name='jobseekerdash'),
    path('jsprofile/',views.jsprofile,name='jsprofile'),
    path('jsupdate/',views.jsupdate,name='jsupdate'),
    path('appliedjobs/',views.appliedjobs,name='appliedjobs'),
    path('save_education/',views.save_education,name='save_education'),
    path('save_experience/',views. save_experience,name='save_experience'),
    path('save_additional/',views. save_additional,name='save_additional'),
    path('jobseekerlogout/',views.jobseekerlogout,name='jobseekerlogout'),
    path('jschangepassword/',views.jschangepassword,name='jschangepassword'),
    path('savedjobs/',views.savedjobs,name='savedjobs'),
    path('save-skills/',views.save_js_skills,name='save_js_skills'),
    path('apply/<int:id>',views.apply,name='apply'),
    
    
]