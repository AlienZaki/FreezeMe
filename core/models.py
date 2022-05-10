from datetime import date
from django.db import models


class Client(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    ssn = models.CharField(max_length=9)
    dob = models.DateField()
    start_freeze_date = models.DateField(null=True, blank=True, default=date.today)
    end_freeze_date = models.DateField(null=True, blank=True)
    id_card = models.ImageField(upload_to='uploads/ID/', null=True, blank=True)
    passport = models.ImageField(upload_to='uploads/Passport/', null=True, blank=True)
    driver_license = models.ImageField(upload_to='uploads/Driver/', null=True, blank=True)
    residency = models.ImageField(upload_to='uploads/Residencies/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f'{self.fname} {self.lname}'

    @property
    def succeed_submissions(self):
        return self.submission_set.filter(finished=True, succeed=True)

    @property
    def failed_submissions(self):
        return self.submission_set.filter(finished=True, succeed=False)

    @property
    def pending_submissions(self):
        return self.submission_set.filter(finished=False)


    def __str__(self):
        return f'{self.fname} {self.lname}'


class Website(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name



class Submission(models.Model):
    FINISHED_CHOICES = [
        (True, 'Finished'),
        (False, 'Processing')
    ]
    SUCCEED_CHOICES = [
        (True, 'Succeed'),
        (False, 'Failed')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(choices=FINISHED_CHOICES, default=False)
    succeed = models.BooleanField(choices=SUCCEED_CHOICES, default=False)

    def __str__(self):
        return f'{self.timestamp}'


class Requirement(models.Model):
    website = models.OneToOneField(Website, on_delete=models.CASCADE)
    fname = models.BooleanField(default=True)
    lname = models.BooleanField(default=True)
    city = models.BooleanField(default=True)
    state = models.BooleanField(default=True)
    zip = models.BooleanField(default=False)
    address_line1 = models.BooleanField(default=True)
    address_line2 = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    email = models.BooleanField(default=True)
    ssn = models.BooleanField(default=True)
    dob = models.BooleanField(default=False)
    start_freeze_date = models.BooleanField(default=False)
    end_freeze_date = models.BooleanField(default=False)
    id_card = models.BooleanField(default=False)
    passport = models.BooleanField(default=False)
    driver_license = models.BooleanField(default=False)
    residency = models.BooleanField(default=False)

    def __str__(self):
        return self.website.name


class Settings(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    def __str__(self):
        return self.name




