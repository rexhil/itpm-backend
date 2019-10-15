from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    dob = models.DateField(null=False)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    mobile = models.CharField(max_length=10, null=False)
    creation_time = models.DateTimeField(default=timezone.now)


class InsuranceType(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name


class InsurancePlan(models.Model):
    insurance_type = models.ForeignKey(InsuranceType, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=True)
    premium = models.FloatField(null=False)
    total = models.FloatField(null=False)
    duration = models.CharField(max_length=100, null=False)
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Insurance Plan(Name: {}, Total: {})'.format(self.name, self.total)


class Insurance(models.Model):
    insurance_plan = models.ForeignKey(InsurancePlan, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=timezone.now)


class Claim(models.Model):
    amount = models.CharField(max_length=40, null=False, unique=False)
    insurance = models.ForeignKey(Insurance, null=False, on_delete=models.CASCADE)
    approval_state = models.CharField(max_length=1,
                                      choices=(('A', 'Approved'), ('N', 'Not approved'), ('P', 'Pending')),
                                      default='P')
    is_active = models.BooleanField(default=True, null=False)
    creation_time = models.DateTimeField(default=timezone.now)
