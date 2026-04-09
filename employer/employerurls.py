from django.urls import path
from . import views



urlpatterns = [
    path('employerdash/',views.employerdash,name='employerdash'),
    path('employerlogout/',views.employerlogout,name='employerlogout'),
    path('updateempprofile/',views.updateempprofile,name='updateempprofile'),
    path('empprofile/',views.empprofile,name='empprofile'),
    path('empviewjobs/',views.empviewjobs,name='empviewjobs'),
    path('emppostjobs/',views.emppostjobs,name='emppostjobs'),
    path('empchangepassword/',views.empchangepassword,name='empchangepassword'),
    path('add_company/',views.add_company,name='add_company'),
    path('viewapplicants/<int:id>',views.viewapplicants,name='viewapplicants'),
    path('empeditjob/<int:id>/', views.empeditjob, name='empeditjob'),
    path('deletejob/<int:id>',views.deletejob,name='deletejob'),
    path('updatestatus/<int:appid>',views.updatestatus,name='updatestatus'),

]