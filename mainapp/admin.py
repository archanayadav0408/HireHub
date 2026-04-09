from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Enquiry )
admin.site.register(UserInfo )
admin.site.register(Jobseeker)
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(JobCategory)
admin.site.register(JobApplication)

