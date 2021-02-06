from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User=get_user_model()

class UsercreationForm(forms.ModelForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Password Confirmation',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields  = ('email', 'first_name', 'last_name')
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if len(password1) < 8:
            raise forms.ValidationError("password must be 8 character")
        elif password1 != password2:
            raise forms.ValidationError("password are not matching")
        return password2
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))

        if commit:
            user.save()
        return user
class UserchangeForm(forms.ModelForm):
    password =ReadOnlyPasswordHashField()
    class Meta:
        model=User
        fields =('email','password','first_name','last_name','is_staff','is_superuser','is_active','is_varified','city',
                 'register_free','purpose'
                 )
    def clean_password(self):
        return self.initial['password']


