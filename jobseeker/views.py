from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from django.utils import timezone
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def jobseekerdash(request):
    if "jsid" not in request.session:
        messages.error(request,"login required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    educations = Education.objects.filter(jobseeker=js)
    experience = Experience.objects.filter(jobseeker=js)
    skills = js.skills.all()
    recommended_jobs = Job.objects.filter(is_active=True)
    recent_applications = JobApplication.objects.filter(jobseeker=js)

    context = {
        'js':js,
        'educations':educations,
        'experience':experience,
        'skills': skills,
        'jobs': recommended_jobs,
        'applications': recent_applications,
    }
    return render(request,'jobseeker/jobseekerdash.html',context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def savedjobs(request):
    if "jsid" not in request.session:
        messages.error(request,"login required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    saved_jobs = SavedJobs.objects.filter(jobseeker = js)
   

    context = {
        'js':js,
        'saved_jobs': saved_jobs
       
    }
    return render(request,'jobseeker/savedjobs.html',context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def jsprofile(request):
    if "jsid" not in request.session:
        messages.error(request,"login required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    educations = Education.objects.filter(jobseeker=js)
    experience = Experience.objects.filter(jobseeker=js)
    skills = js.skills.all()

    context = {
        'js':js,
        'educations':educations,
        'experience':experience,
          'skills': skills,
    }
    return render(request,'jobseeker/jsprofile.html',context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def jsupdate(request):
    if "jsid" not in request.session: 
        messages.error(request,"login required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    educations = Education.objects.filter(jobseeker=js)
    experience = Experience.objects.filter(jobseeker=js)
    
    context = {
        'js':js,
        'educations':educations,
        'experience':experience,
       
    }
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dob  = request.POST.get('dob')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        contact_no = request.POST.get('contact_no')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')
        picture = request.FILES.get('picture')
        
        js.first_name = firstname
        js.last_name = lastname
        js.dob = dob
        js.gender = gender
        js.email = email
        js.contact_no = contact_no
        js.locality = locality
        js.city = city
        js.zip_code = zip_code
        js.district = district
        js.state = state
        js.country = country
        
        if picture:
            js.picture = picture
        js.save()
       
        messages.success(request,"Profile Updated")
        return redirect('jsupdate')
    return render(request,'jobseeker/jsupdate.html',context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def appliedjobs(request):
    if "jsid" not in request.session:
        messages.error(request,"login required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    appliedjob = JobApplication.objects.filter(jobseeker=js)
    return render(request,'jobseeker/appliedjobs.html',{'appliedjob':appliedjob,'js':js})

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def save_education(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == 'POST':
        degree_name = request.POST.get('degree_name')
        specialization = request.POST.get('specialization')
        institute = request.POST.get('institute')
        university = request.POST.get('university')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        Education.objects.create(jobseeker=js,degree_name=degree_name,specialization=specialization,institute=institute,university=university,start_year=start_year,end_year=end_year)
        messages.success(request,"Education Added Successfully")
        return redirect('jsupdate')


    else:
        messages.error(request,"Something Went Wrong")
        return redirect('login')
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def jobseekerlogout(request):
    if 'jsid' not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    del request.session['jsid']
    messages.success(request,'Logout Successfully')
    return redirect('index')
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def save_experience(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        designation = request.POST.get('designation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        Experience.objects.create(jobseeker=js,company_name=company_name,designation=designation,start_date=start_date,end_date=end_date,description=description)
        messages.success(request,"Experience added Successfully")
        return redirect('jsupdate')
    else:
        messages.error(request,"Something Went Wrong")
        return redirect('login')
    
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def save_additional(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        resume = request.FILES.get('resume')
        if resume:
            js.resume = resume
        cv = request.FILES.get('cover_letter')
        if cv:
            js.cover_letter = cv
        js.expected_salary = request.POST.get('expected_salary')
        js.current_salary = request.POST.get('current_salary')
        js.notice_period = request.POST.get('notice_period')
        js.linkedin_url = request.POST.get('linkedin_url')
        js.github_url = request.POST.get('github_url')
        js.portfolio_url = request.POST.get('portfolio_url')
        work = request.POST.get('is_open_to_work')
        if work=='on':
            js.is_open_to_work = True
        else:
            js.is_open_to_work = False
        js.save()
        messages.success(request,"Additional Details Saved")
        return redirect('jsupdate')
    else:
        messages.warning(request,"Something went Wrong")
        return redirect('index')

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def save_js_skills(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')

    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)

    if request.method == "POST":
        skills_input = request.POST.get('skills')

        if skills_input:
            skill_objects = []
            skill_names = [s.strip() for s in skills_input.split(',') if s.strip()]

            for name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    skill_name__iexact=name,
                    defaults={'skill_name': name}
                )
                skill_objects.append(skill)

            js.skills.set(skill_objects)

            messages.success(request, "Skills Updated Successfully")
        else:
            js.skills.clear()
            messages.warning(request, "All skills removed")

        return redirect('jsupdate')

    return redirect('jsupdate')


@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def apply(request,id):
    if "jsid" not in request.session:
        messages.error(request,"you must be logged in before applying any job")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    job = Job.objects.get(id=id)

    if job.is_active == False:
        return redirect('jobdetails',id=job.id)
    if job.deadline < timezone.now().date():
        messages.error(request,"Deadline has been Passed")
        return redirect('jobdetails',id = job.id)
    

    if JobApplication.objects.filter(jobseeker=js,job=job):
        messages.warning(request,"you have already applied for this job")
        return redirect('jobdetails', id=job.id)


    JobApplication.objects.create(
        jobseeker = js,
        job = job
    )



    messages.success(request,"Applied Successfully , You can also track the application status ")
    return redirect('jobdetails', id=job.id)


@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def jschangepassword(request):
    if "jsid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    context = {
        'jsid' : jsid,
        'js':js
    }
    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        employer = UserInfo.objects.get(username = jsid)
        if newpwd != confirmpwd:
            messages.warning(request,"New and confirm Password not matched ")
            return redirect('changepassword')
        elif employer.password != oldpwd :
            messages.error(request,"old password didn't matched")
            return redirect('changepassword')
        elif employer.password == newpwd:
            messages.warning(request,"Password cannot be same as previous passwords. ")
            return redirect('changepassword')
        else:
            employer.password = newpwd
            employer.save()
            messages.success(request,"Password Changed Successfully")
            return redirect('jobseekerdash')
     
    return render(request,"jobseeker/jschangepassword.html",context)
