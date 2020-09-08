from fieldsignals import post_save_changed

from leaves.models import Holiday, LeaveApplication


def calculate_leave_business_days(sender, instance, created, using, changed_fields=None, **kwargs):
    fields = ("from_date", "to_date")
    date_fields_updated = any([f in changed_fields for f in fields])
    if created or date_fields_updated:
        business_days_count = Holiday.business_days_count(instance.from_date, instance.to_date)
        instance.count = business_days_count
        instance.save()
    
post_save_changed.connect(calculate_leave_business_days, sender=LeaveApplication)