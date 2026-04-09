from django.db import models


# Create your models here.
class Enquiry(models.Model):
    name = models.CharField(max_length= 100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry by - {self.name} - {self.contact}"
    
class UserInfo(models.Model):
    UTYPE = (('jobseeker','Job seeker'),('employer','Employer'),('admin','Admin'))
    usertype = models.CharField(max_length=15,choices=UTYPE)
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=256)



class Skill(models.Model):
   
    skill_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill_name}"


class Jobseeker(models.Model):
    GENDER_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
        ('na', 'Prefer not to say'),
    )
    
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, related_name="jobseeker")

    # Personal Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    # Address
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")

    # Files
    picture = models.ImageField(upload_to="jobseeker_profiles/", blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    cover_letter = models.FileField(upload_to="cover_letters/", blank=True, null=True)

    # Skills (Many-to-Many)
    skills = models.ManyToManyField(Skill, related_name="jobseekers")

    # additional
    expected_salary = models.IntegerField(blank=True, null=True)
    current_salary = models.IntegerField(blank=True, null=True)
    notice_period = models.IntegerField(help_text="In days", blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    is_open_to_work = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Education(models.Model):
    jobseeker = models.ForeignKey(Jobseeker, on_delete=models.CASCADE, related_name="educations")
    degree_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    institute = models.CharField(max_length=200)
    university = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.degree_name} - {self.jobseeker}"

class Experience(models.Model):
    jobseeker = models.ForeignKey(Jobseeker, on_delete=models.CASCADE, related_name="experiences")
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.company_name} - {self.jobseeker}"
    
class Company(models.Model):
    
    company_name = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.TextField()
    logo = models.ImageField(upload_to="company_logo/",blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    industry = models.CharField(max_length=100,help_text="Sector")
    established_at = models.DateField(null=True)
    details = models.TextField(null=True,blank=True, help_text="Company description")



    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.industry}"
    
class Employer(models.Model):
     GENDER_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
        ('na', 'Prefer not to say'),
    )
    
    
     user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, related_name="employer")
     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company",null=True)

    # Personal Details
     first_name = models.CharField(max_length=100)
     last_name = models.CharField(max_length=100)
     dob = models.DateField(null=True)
     gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
     contact_no = models.CharField(max_length=15)
     email = models.EmailField(unique=True)
     designation = models.CharField(max_length=200)
     picture = models.ImageField(upload_to="employer_profiles", blank=True, null=True)



     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
        return self.user.username
     
class JobCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.category_name


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    )

    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,related_name="jobs")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name="jobs",null=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)

    salary = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=200)

    skills_required = models.ManyToManyField(Skill, related_name="jobs")

    vacancy = models.IntegerField(default=1)
    deadline = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    jobseeker = models.ForeignKey(
        Jobseeker,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected'),
            ('selected', 'Selected'),
        ),
        default='pending'
    )

    def __str__(self):
        return f"{self.jobseeker} - {self.job}"


class SavedJobs(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="saved"
    )

    jobseeker = models.ForeignKey(
        Jobseeker,
        on_delete=models.CASCADE,
        related_name="saved"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job', 'jobseeker'], name='unique_saved_job')
        ]
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jobseeker} - {self.job}"
    

     



    

