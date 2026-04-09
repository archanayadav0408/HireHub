from django.shortcuts import render, redirect
from .models import *
from .forms import EnquiryForm
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
import random
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail


def forgot_password(request):
    
    context = {

    }

    # STEP 1 → send OTP
    if request.method == "POST" and 'send_otp' in request.POST:
        email = request.POST.get('email')

        try:
            user = UserInfo.objects.get(username=email)

            otp = str(random.randint(100000, 999999))

            # store in session (temporary storage)
            request.session['otp'] = otp
            request.session['email'] = email

            send_mail(
                f'Your OTP Code',
                f'Your OTP is {otp}',
                'archanayadav040896@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request,"Otp sent successfully.")
            context['show_otp'] = True

        except UserInfo.DoesNotExist:
            messages.error(request,"Email not found")

    # STEP 2 → verify OTP and change password
    elif request.method == "POST" and 'verify_otp' in request.POST:
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('password')

        if entered_otp == request.session.get('otp'):
            user = UserInfo.objects.get(username=request.session.get('email'))
            user.password = new_password
            user.save()

            messages.success(request,"Password changed successfully")
            return redirect('login')
        else:
            messages.error(request,"Wrong otp")
            context['show_otp'] = True

    return render(request, 'mainapp/forgot_password.html', context)
# Create your views here.
def index(request):
   job = Job.objects.all().order_by('-created_at')[:5]
   userid = request.session.get('jsid') or request.session.get('empid') or request.session.get('adminid')
   user = None
   if userid:
       obj = UserInfo.objects.get(username=userid)
       if obj.usertype == "jobseeker":
           user = Jobseeker.objects.get(email=userid)
       elif obj.usertype == "employer" :
           user = Employer.objects.get(email=userid)
       elif obj.usertype == "admin" :
           user = UserInfo.objects.get(username=userid)
    
   context = {
       "job":job,
       "is_home": True,
       "user":user
   }
   return render(request,'mainapp/index.html',context)

def jobs(request):
    userid = request.session.get('jsid') or request.session.get('empid') or request.session.get('adminid')
    user = None
    if userid:
        obj = UserInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer" :
            user = Employer.objects.get(email=userid)
        elif obj.usertype == "admin" :
            user = UserInfo.objects.get(username=userid)
    job = Job.objects.all()
    title = request.GET.get('title')
    location = request.GET.get('location')

    if title:
       job = job.filter(title__icontains=title)

    if location:
       job = job.filter(location__icontains=location)

    paginator = Paginator(job, 2)
    page_number = request.GET.get('page')
    jobFinal = paginator.get_page(page_number)
    for j in job:
        if j.deadline < timezone.now().date():
            j.is_active = False
            j.save()
    context = {
        'job':jobFinal,
        'user':user,
        "is_home": True,
        "user":user
    }  
    return render(request, "mainapp/jobs.html",context)

def login(request):
    
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = UserInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer" :
            user = Employer.objects.get(email=userid)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserInfo.objects.get(username=username, password=password)
            if user and user.usertype == 'admin':
                messages.success(request,'welcome Admin')
                request.session['adminid'] = user.username
                request.session.set_expiry(0)
                return redirect('admin_dash')
            elif user and user.usertype == 'jobseeker':
                js = Jobseeker.objects.get(email=user.username)
                messages.success(request,f"Welcome {js.first_name}")
                request.session['jsid'] = user.username
                request.session.set_expiry(0)
                return redirect('index')
                
            elif user and user.usertype == 'employer':
                emp = Employer.objects.get(email=user.username)
                messages.success(request,f"Welcome {emp.first_name}")
                request.session['empid'] = user.username
                request.session.set_expiry(0)
                return redirect('index')
                
        except UserInfo.DoesNotExist:
            messages.error(request,"Invalid Username or Password")
            return redirect('login')
            
    return render(request,'mainapp/login.html',{'user':user})

def register(request):
    if request.method == "POST":
        usertype = request.POST.get('usertype')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.warning(request,'Password must be same.')
            return redirect('register')
        exist =UserInfo.objects.filter(username = email)
        if exist:
            messages.error(request,'This email is already registered')
            return redirect('register')
        try:
            with transaction.atomic():
                log = UserInfo(usertype=usertype,username=email,password=password)
                if usertype=="jobseeker":
                    js = Jobseeker(user=log,first_name=firstname,last_name=lastname,email=email,contact_no=contact_no)
                    log.save()
                    js.save()
                elif usertype=="employer":
                    emp = Employer(user=log,first_name=firstname,last_name=lastname,email=email,contact_no=contact_no)
                    log.save()
                    emp.save()

                messages.success(request,"Registered Successfully. Now login to update profile!")
                return redirect('login')
        except Exception as e:
            messages.error(request,'Something went wrong.')
            return redirect('register')
    return render(request,'mainapp/register.html')

def about(request):
    userid = request.session.get('jsid') or request.session.get('empid') or request.session.get('adminid')
    user = None
    if userid:
        obj = UserInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer" :
            user = Employer.objects.get(email=userid)
        elif obj.usertype == "admin" :
            user = UserInfo.objects.get(username=userid)
        
    context = {
        "is_home": True,
        "user":user
    }
    return render(request,'mainapp/about.html',context)

def contact(request):
    userid = request.session.get('jsid') or request.session.get('empid') or request.session.get('adminid')
    user = None
    if userid:
        obj = UserInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer" :
            user = Employer.objects.get(email=userid)
        elif obj.usertype == "admin" :
            user = UserInfo.objects.get(username=userid)
        
    
    if request.method == "POST":
        data = EnquiryForm(request.POST)
        if data.is_valid():
            data.save()
            messages.success(request,"Enquiry Sent Successfully")
            return redirect('contact')
        else:
            messages.error(request,"Failed to sent enquiry, Invalid form data")
            form = EnquiryForm()
        return redirect('contact')
    else:
       
        form = EnquiryForm()
    context = {
        "is_home": True,
        "user":user,
        "form":form
    }
    return render(request,'mainapp/contact.html',context)

def savedjob(request,id):
    userid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=userid)
    if userid:
        job = Job.objects.get(id=id)
        obj, created = SavedJobs.objects.get_or_create(job = job, jobseeker = js)
        messages.success(request,"Saved to Whislist")
        if not created:
            messages.warning(request,"Already Saved")
        return redirect('jobs')
    else:
        messages.error(request,"Please Login First")
        return redirect('jobs')
    


def jobdetails(request,id):
    job = Job.objects.get(id=id)   
    userid = request.session.get('jsid') or request.session.get('empid') or request.session.get('adminid')
    user = None
    if userid:
        obj = UserInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer" :
            user = Employer.objects.get(email=userid)
        elif obj.usertype == "admin" :
            user = UserInfo.objects.get(username=userid)
    context = {
       "job":job,
      
       "user":user
   }
   
    return render(request, "mainapp/jobdetails.html",context)

