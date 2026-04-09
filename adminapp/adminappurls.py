from django.urls import path
from .import views
urlpatterns = [
   path('admin_dash/',views.admin_dash,name='admin_dash'),
   path('viewenq/',views.viewenq,name='viewenq'),
   path('delenq/<id>',views.delenq,name='delenq'),
   path('changepassword/',views.changepassword,name='changepassword'),
   path('adminlogout/',views.adminlogout,name='adminlogout'),
   path('addcat/',views.addcat,name='addcat'),
   path('viewcat/',views.viewcat,name='viewcat'),
   path('jobseeker/',views.jobseeker,name='jobseeker'),
   path('employer/',views.employer,name='employer'),

]