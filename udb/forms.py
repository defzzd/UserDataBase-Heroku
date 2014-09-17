from django import forms



class CreateUserForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100, required=False)
    email_address = forms.EmailField(label='Email address', max_length=100)
    
    
class EditUserForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100, required=False)
    last_name = forms.CharField(label='Last name', max_length=100, required=False)
    email_address = forms.EmailField(label='Email address', max_length=100, required=False)
    