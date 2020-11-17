from calendar import monthrange

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import HolidayTemplate

class HolidayTemplateAdminForm(forms.ModelForm):
    class Meta:
        model = HolidayTemplate
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data
        day = cleaned_data.get("day")
        month = cleaned_data.get("month")
        
        if month not in range(1, 12):
            raise forms.ValidationError(_("Invalid Month input."))
        
        month_days = monthrange(2020, month)[1]
        if day not in range(1, month_days):
            raise forms.ValidationError(_("Day out of range from month."))
        return cleaned_data
