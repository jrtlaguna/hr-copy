from django.db.models.signals import pre_save
from django.dispatch import receiver

from leaves.models import Holiday, LeaveApplication

@receiver(pre_save, sender=LeaveApplication)
def calculate_leave_business_days(sender, raw, instance, **kwargs):
    business_days_count = Holiday.business_days_count(instance.from_date, instance.to_date)
    instance.count = business_days_count
    
