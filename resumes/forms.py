from django import forms

ROLE_CHOICES = [
    ('backend', 'Backend Developer'),
    ('frontend', 'Frontend Developer'),
    ('fullstack', 'Full Stack Developer'),
    ('intern', 'Intern'),
    ('data_scientist', 'Data Scientist'),
    ('product_manager', 'Product Manager'),
    ('designer', 'Designer'),
    ('python_developer', 'Python Developer'),
    ('java_developer', 'Java Developer'),
    ('mobile_app_developer', 'Mobile App Developer'),
    ('devops_engineer', 'DevOps Engineer'),
    ('cloud_engineer', 'Cloud Engineer'),
    ('ai_ml_engineer', 'AI / ML Engineer'),
    ('data_analyst', 'Data Analyst'),
    ('qa_test_engineer', 'QA / Test Engineer'),
    ('automation_engineer', 'Automation Engineer'),
    ('site_reliability_engineer', 'Site Reliability Engineer'),
    ('game_developer', 'Game Developer')
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
