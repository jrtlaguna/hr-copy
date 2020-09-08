from fieldsignals import post_save_changed

from leaves.models import Holiday, LeaveApplication
from django.dispatch import receiver


@receiver(post_save_changed, sender=LeaveApplication)
def calculate_leave_business_days(sender, instance, created, changed_fields=None, **kwargs):
    fields = ("from_date", "to_date")
    date_fields_updated = any([field in changed_fields for field in fields])
    if created or date_fields_updated:
        business_days_count = Holiday.business_days_count(instance.from_date, instance.to_date)
        instance.count = business_days_count
        instance.save()