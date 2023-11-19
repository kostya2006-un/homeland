from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50,label="Имя")
    last_name = forms.CharField(max_length=50,label="Фамилия")

    def save(self, request):
        user = super(CustomSignupForm,self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user