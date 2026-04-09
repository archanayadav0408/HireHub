from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def employerdash(request):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.select_related("company").get(email=empid)
    jobs = Job.objects.filter(employer=emp)
    total_jobs = jobs.count()
    active_jobs = jobs.filter(
        is_active=True,
    ).count()
    closed_jobs = jobs.filter(
        is_active = False,
    ).count()
    applications = JobApplication.objects.filter(job__employer=emp).count()
    recent_jobs = jobs.order_by('-created_at')[:5]
    recent_applications = JobApplication.objects.filter(
        job__employer=emp
    )

    context = {
        "emp": emp,
        "empid": empid,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "closed_jobs": closed_jobs,
        "applications": applications,
        "jobs": recent_jobs,
        "recent_applications": recent_applications,
    }

    return render(request, "employer/employerdash.html", context)
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def empprofile(request):
    if "empid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    context = {
        'empid':empid,
        'emp':emp
    }
    return render(request,"employer/empprofile.html",context)


@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def updateempprofile(request):
    if "empid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    context = {
        'empid':empid,
        'emp':emp
    }
    if request.method == "POST":
        emp.first_name = request.POST.get('firstname')
        emp.last_name = request.POST.get('lastname')
        emp.dob  = request.POST.get('dob')
       
        emp.gender = request.POST.get('gender')
        emp.contact_no = request.POST.get('contact_no')
        picture = request.FILES.get('picture')
        if picture:
            emp.picture = picture
        emp.designation = request.POST.get('designation')
        emp.save()
        messages.success(request,"Profile updated successfully")
        return redirect('updateempprofile')
    return render(request,"employer/updateempprofile.html",context)
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def empviewjobs(request):
    if "empid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    emp_jobs = Job.objects.filter(employer=emp)
   
    context = {
        'empid':empid,
        'emp':emp,
        'emp_jobs':emp_jobs
    }
    return render(request,"employer/empviewjobs.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def emppostjobs(request):
    if "empid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    all_skills = Skill.objects.all()
    categ = JobCategory.objects.all()
    context = {
        'empid':empid,
        'emp':emp,
        'all_skills':all_skills,
        'categ':categ
    }
    
    if request.method == 'POST':
        cat = None
        catid = request.POST.get('catid')
        if catid:
            cat = JobCategory.objects.get(id=catid)
        title = request.POST.get('title')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        vacancy = request.POST.get('vacancy')
        deadline = request.POST.get('deadline')
        skills_required = request.POST.get('skills_required')
        description = request.POST.get('description')
        if not emp.company:
            messages.warning(request,"You haven't added company information yet")
            return redirect('emppostjobs')
        job = Job.objects.create(category=cat,employer=emp,company=emp.company,title=title,job_type=job_type,salary=salary,location=location,vacancy=vacancy,deadline=deadline,description=description)
        if skills_required:
            job_skill = []
            skill_names = [s.strip()  for s in skills_required.split(',') if s.strip()]
            for name in skill_names:
                skill, created = Skill.objects.get_or_create( 
                    skill_name__iexact = name,defaults={'skill_name':name}
                     )
                job_skill.append(skill)
            job.skills_required.set(job_skill)
        job.save()
        messages.success(request,"Job posted successfully")
        return redirect('emppostjobs')

    return render(request,"employer/emppostjobs.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def empchangepassword(request):
    if "empid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    context = {
        'empid' : empid,
        'emp' : emp
    }
    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        employer = UserInfo.objects.get(username = empid)
        if newpwd != confirmpwd:
            messages.warning(request,"New and confirm PAssword not matched ")
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
            return redirect('employerdash')
     
    return render(request,"employer/empchangepassword.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def employerlogout(request):
    if 'empid' not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    del request.session['empid']
    messages.success(request,'Logout Successfully')
    return redirect('index')

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def add_company(request):
     if "empid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
     empid = request.session.get('empid')
     emp = Employer.objects.get(email=empid)
     if request.method == "POST":
         company_name = request.POST.get('company_name')
         contact_no = request.POST.get('contact_no')
         email = request.POST.get('email')
         logo = request.FILES.get('logo')
         industry = request.POST.get('industry')
         established_at = request.POST.get('established_at')
         website = request.POST.get('website')
         location = request.POST.get('location')
         details = request.POST.get('details')
         comp = Company.objects.create(company_name=company_name, contact_no=contact_no, email=email,logo=logo,industry=industry,established_at=established_at,website=website,location=location,details=details)
         emp.company = comp
         emp.save()
         messages.success(request,"Company added successfully.")
         return redirect('updateempprofile')
     else:
         messages.error(request,"Something went wrong")
         return redirect('login')
     
@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def viewapplicants(request, id):
     if "empid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
     empid = request.session.get('empid')
     emp = Employer.objects.get(email=empid)
     job = Job.objects.get(id=id)
     applications = JobApplication.objects.filter(job=job)
     context = {
         'empid': empid,
         'emp' : emp,
         'job': job,
         'applications':applications
     }
     return render(request, "employer/viewapplicants.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def empeditjob(request, id):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')

    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)

    job = Job.objects.get(id=id, employer=emp)

    all_skills = Skill.objects.all()

    context = {
        "emp": emp,
        "job": job,
        "all_skills": all_skills
    }

    if request.method == "POST":
        job.title = request.POST.get('title')
        job.job_type = request.POST.get('job_type')
        job.salary = request.POST.get('salary')
        job.location = request.POST.get('location')
        job.vacancy = request.POST.get('vacancy')
        job.deadline = request.POST.get('deadline')
        job.description = request.POST.get('description')

        skills_required = request.POST.get('skills_required')

        if skills_required:
            job_skill = []
            skill_names = [s.strip() for s in skills_required.split(',') if s.strip()]

            for name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    skill_name__iexact=name,
                    defaults={'skill_name': name}
                )
                job_skill.append(skill)

            job.skills_required.set(job_skill)

        job.save()

        messages.success(request, "Job updated successfully")
        return redirect('empviewjobs')

    return render(request, "employer/empeditjob.html", context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def  deletejob(request,id):
    job = Job.objects.get(id=id)
    job.delete()
    messages.success(request,"job deleted")
    return redirect('empviewjobs')

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def updatestatus(request, appid):
      if "empid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
      app = JobApplication.objects.get(id=appid)
      if request.method == "POST":
          status = request.POST.get('status')
          app.status = status
          app.save()
          if status == 'selected':
              try:
                  
                send_mail(
                  f"Selection Confirmation for the Position Applied -Hirehub",
                  f"""
                  Dear {app.jobseeker.first_name}{app.jobseeker.last_name},
                  We Are Pleased to inform you that you have been selected for the position of {app.job.title} 
                  Please confirm your acceptance and share your availability for joining.
                  Best Regards,
                  {app.job.employer.first_name}{app.job.employer.last_name}
                  {app.job.employer.company.company_name} """,
                  f"archanayadav040896@gmail.com",
                  [app.jobseeker.email],
                  fail_silently=False,
              )
              except:
                  messages.warning(request,"Status Updated but can't send mail,")
          messages.success(request,"Application status updated")
          return redirect('viewapplicants',id=app.job.id)
      else:
           return redirect('viewapplicants',id=app.job.id)
          
    
   