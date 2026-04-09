from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from django.views.decorators.cache import cache_control
# Create your views here.

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def admin_dash(request):
    if "adminid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid
    }
    return render(request,"admin/admin_dash.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def addcat(request):
    if "adminid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid
    }
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        if JobCategory.objects.filter(category_name__iexact = category_name):
            messages.warning(request,"Category Already exist")
            return redirect('addcat')
        JobCategory.objects.create(category_name=category_name)
        messages.success(request, "Category Added successfully")
    return render(request,"admin/addcat.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def viewcat(request):
    if "adminid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    adminid = request.session.get('adminid')
    category = JobCategory.objects.all()
    context = {
        'adminid' : adminid,
        'category':category
    }
    return render(request,"admin/viewcat.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def jobseeker(request):
    if "adminid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    adminid = request.session.get('adminid')
    js = Jobseeker.objects.all()
    context = {
        'adminid' : adminid,
        'js':js
    }
    return render(request,"admin/jobseeker.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def employer(request):
    if "adminid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    adminid = request.session.get('adminid')
    emp = Employer.objects.all()
    context = {
        'adminid' : adminid,
        'emp':emp
    }
    return render(request,"admin/employer.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def viewenq(request):
    if "adminid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    adminid = request.session.get('adminid')
    e = Enquiry.objects.all()
    context = {
        'adminid': adminid ,
        'enqs':e
    }
    return render(request,"admin/viewenq.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def delenq(request,id):
    e = Enquiry.objects.get(id=id)
    e.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('viewenq')

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def changepassword(request):
    if "adminid" not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid
    }
    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        admin = UserInfo.objects.get(username = adminid)
        if newpwd != confirmpwd:
            messages.warning(request,"New and confirm PAssword not matched ")
            return redirect('changepassword')
        elif admin.password != oldpwd :
            messages.error(request,"old password didn't matched")
            return redirect('changepassword')
        elif admin.password == newpwd:
            messages.warning(request,"Password cannot be same as previous passwords. ")
            return redirect('changepassword')
        else:
            admin.password = newpwd
            admin.save()
            messages.success(request,"Password Changed Successfully")
            return redirect('admin_dash')
     
    return render(request,"admin/changepassword.html",context)

@cache_control(no_store=True, no_cache=True, must_relvalidate=True)
def adminlogout(request):
    if 'adminid' not in request.session:
        messages.error(request,"Login First")
        return redirect('login')
    del request.session['adminid']
    messages.success(request,'Logout Successfully')
    return redirect('index')
