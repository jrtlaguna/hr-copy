from django.contrib import admin
from .models import (
    Employee,
    Education, 
    EmergencyContact,
    WorkHistory,
    User
    )

# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Education)
admin.site.register(WorkHistory)
admin.site.register(EmergencyContact)