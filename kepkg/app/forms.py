from django import forms
from django.contrib.auth.models import User
from .models import Profile, Submission, Status, Review, Reviewer, Decision, Resubmission, Amandement, News
from bootstrap_datepicker_plus.widgets  import DatePickerInput
from django_select2.forms import Select2Widget, Select2MultipleWidget
from ckeditor.widgets import CKEditorWidget


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password tidak sama.')
        return cd['password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fullname', 'photo', 'dob', 'gender', 'address', 'city', 'phone', 'mobile')

        widgets = {
            'dob': DatePickerInput()
        }

class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = '__all__'
        exclude = ['user' ]


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'
        exclude = ['submission']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('description', 'file_review', 'decision', 'review_date')

        widgets = {
            'review_date': DatePickerInput(),
        }


class DecisionForm(forms.ModelForm):

    class Meta:
        model = Decision
        fields = '__all__'
        exclude = ['submission', 'created_at'  ]



class ReviewerForm(forms.ModelForm):

    class Meta:
        model = Reviewer
        fields = ('reviewer',)


        widgets = {
            'reviewer': Select2Widget,
        }


class ResubmissionForm(forms.ModelForm):

    class Meta:
        model = Resubmission
        fields = '__all__'
        exclude = ['submission', 'review'  ]


class ResubmissionUpdateForm(forms.ModelForm):

    class Meta:
        model = Resubmission
        fields = '__all__'
        exclude = ['submission'  ]


class AmandementForm(forms.ModelForm):

    class Meta:
        model = Amandement
        fields = '__all__'
        exclude = ['submission', 'review'  ]


class AmandementUpdateForm(forms.ModelForm):

    class Meta:
        model = Amandement
        fields = '__all__'
        exclude = ['submission'  ]


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = [ 'created_at'  ]



