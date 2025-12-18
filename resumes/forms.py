from django import forms

ROLE_CHOICES = [
    ('backend', 'Backend Developer'),
    ('frontend', 'Frontend Developer'),
    ('fullstack', 'Full Stack Developer'),
    ('intern', 'Intern'),
]

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".pdf, application/pdf"})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def clean_resume(self):
        file = self.cleaned_data['resume']

        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")

        if file.size > 2 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 2MB.")

        return file
