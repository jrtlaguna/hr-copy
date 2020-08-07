from allauth.account.adapter import get_adapter, DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.middle_name = data.get("middle_name")
        user.save()
        return user
