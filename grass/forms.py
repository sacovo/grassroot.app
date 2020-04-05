from django import forms

from django_select2.forms import Select2MultipleWidget

from geopy.geocoders import Nominatim

from grass.models import Category


class SignupForm(forms.Form):
    group_name = forms.CharField(max_length=100)
    categories = forms.ModelMultipleChoiceField(
        Category.objects.all(),
        widget=Select2MultipleWidget,
        required=False,
    )

    zip_code = forms.CharField(max_length=4)
    city = forms.CharField(max_length=180)

    def clean(self):
        cleaned_data = super().clean()

        geolocator = Nominatim(user_agent="django/grassroot.app")
        location = geolocator.geocode(
            cleaned_data['zip_code'] + ' ' + cleaned_data['city']
        )
        cleaned_data['location'] = location
        cleaned_data['lat'] = location.latitude
        cleaned_data['lng'] = location.longitude


class DescriptionStep(forms.Form):
    description = forms.CharField(widget=forms.Textarea)


class MissionStep(forms.Form):
    mission = forms.CharField(widget=forms.Textarea)
