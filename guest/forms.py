from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField, Reset, Button, Div, HTML

class ContactUsForm(forms.Form):
    guest_name = forms.CharField(label='Name')
    guest_email = forms.EmailField(label='E-mail')
    guest_subject = forms.CharField(label='Subject')
    guest_message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'height':'200px', 'style':'resize:none'}))
    guest_attachment = forms.FileField(label='Attachment', required=False, help_text='File upload may take a while, please wait until you get redirected mail success page.')

    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('guest_send_email')
        self.helper.layout = Layout(
            Row('guest_name', css_class = 'col-md-12'),
            Row('guest_email', css_class = 'col-md-12'),
            Row('guest_subject', css_class = 'col-md-12'),
            Row('guest_message', css_class = 'col-md-12'),
            Row('guest_attachment', css_class = 'col-md-12'),
            Submit('submit', 'Send', css_class = 'btn-secondary'),
            Reset('reset', 'Reset', css_class = 'btn-warning'),
            )
