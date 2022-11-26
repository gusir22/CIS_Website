# emailmanager/forms.py
from django import forms
from django.core.validators import RegexValidator


class ContactForm(forms.Form):
    """Form used for the public contact view at /contact/success"""
    full_name = forms.CharField(
        required=True,
        label="Your Full Name",
        max_length=50,
    )
    phone_number = forms.CharField(
        max_length=12,
        help_text="Please, use the xxx-xxx-xxxx format.",
        validators=[
             RegexValidator(r'\d+-\d+-\d+', 'Please enter a valid phone number in the xxx-xxx-xxxx format.'),
        ],
    )
    contact_email = forms.EmailField(
        required=True,
        label="Your Email",
        help_text="The email you would like us to reach you with."
    )
    subject = forms.CharField(required=True, max_length=75)
    message = forms.CharField(widget=forms.Textarea, required=True)

    # def send_email(self):
    #     # send email using the self.cleaned_data dictionary
    #     pass


class RequestAppointmentForm(forms.Form):
    repeat_customer = forms.BooleanField(label='Repeat Customer', required=False)
    pool_code = forms.BooleanField(label='I Have A Pool', required=False)
    owner_permit = forms.BooleanField(label='I Have A Permit', required=False)
    name = forms.CharField(label='Full Name', max_length=60)
    phone_number = forms.CharField(label='Contact Number', max_length=15)
    street_address = forms.CharField(label='Street Address', max_length=120)
    city = forms.CharField(label='City', max_length=60)
    zip_code = forms.CharField(label='Zip Code', max_length=5)
    project_description = forms.CharField(
        label='Project Description', max_length=250,
        required=False, widget=forms.Textarea,
        help_text='Tell us what you need help with'
    )
