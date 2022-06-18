from django import forms
from .models import Profile


# Form to capture/display delivery details on profile
# (copied from latest order if selected)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('basic_phone', 'basic_postcode', 'basic_city',
                  'basic_street1', 'basic_street2',
                  'basic_county', 'basic_country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'basic_phone': 'Phone',
            'basic_postcode': 'Postal Code',
            'basic_city': 'City',
            'basic_street1': 'Street Line 1',
            'basic_street2': 'Street Line 2',
            'basic_county': 'County / State / Locality',
        }

        self.fields['basic_phone'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'basic_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
