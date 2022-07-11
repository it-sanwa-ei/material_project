from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField, Reset, Button, Div, HTML

from .models import CustomUser 

class CustomUserCreationForm(UserCreationForm):
    dept_code = forms.CharField(label='Department Code')
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Column('username', css_class = 'col-md-6'),
                Column('dept_code', css_class = 'col-md-6'),
                css_class='row'
            ),
            Row('email', css_class='col-md-12'),
            Row(Column('password1', css_class = 'col-md-6'),
                Column('password2', css_class = 'col-md-6'),
                css_class='row'),
            Submit('submit', 'Register', css_class='btn btn-primary'),
            Reset('reset', 'Reset', css_class='btn btn-warning')
        )
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:   
        model = CustomUser
        fields = ('username', 'email','department')