# pages/forms.py
from django import forms
from django.core.validators import RegexValidator


class RequestEstimateForm(forms.Form):

    name = forms.CharField(label='Full Name', max_length=60)
    phone_number = forms.CharField(
        label='Contact Number',
        max_length=15,
        validators=[
             RegexValidator(r'\d+-\d+-\d+', 'Please enter a valid phone number in the xxx-xxx-xxxx format.'),
        ],
    )
    contact_email = forms.EmailField(
        required=True,
        label="Your Email",
        help_text="The email you would like us to reach you with."
    )
    street_address = forms.CharField(label='Street Address', max_length=120)
    city = forms.CharField(label='City', max_length=60)
    zip_code = forms.CharField(label='Zip Code', max_length=5)
    product_interest = forms.CharField(label='Product of Interest', max_length=100)
    pool_code = forms.BooleanField(label='I am trying to enclose a pool in this project', required=False)
    owner_permit = forms.BooleanField(label='I will be responsible for acquiring my own permits', required=False)
    hoa_flag = forms.BooleanField(label='The property belongs to an HOA', required=False)
    project_description = forms.CharField(
        label='Project Description', max_length=250,
        required=False, widget=forms.Textarea,
        help_text='Tell us what you need help with'
    )