from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

class SignUpForm(SignupForm):
    
    first_name = forms.CharField(label=_("نام"), max_length=65, required=True)
    last_name = forms.CharField(label=_("نام خانوادگی"), max_length=65, required=True)

    # Override the init method
    def __init__(self, *args, **kwargs):
        # Call the init of the parent class
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"autofocus": "true"})
        self.fields["first_name"].widget.attrs.update({"autofocus": "true"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({"placeholder": ""})
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # Put in custom signup logic
    def custom_signup(self, request, user):
        # Set the user's type from the form reponse
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.full_name = f'{self.cleaned_data["first_name"]} {self.cleaned_data["last_name"]}'
        # Save the user's type to their database record
        user.save()

    
