from django.contrib import admin
from .models import UserInfo, Insurance, InsurancePlan, InsuranceType, Claim

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Insurance)
admin.site.register(InsurancePlan)
admin.site.register(InsuranceType)
admin.site.register(Claim)
