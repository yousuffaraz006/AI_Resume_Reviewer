from django.urls import path
from .views import *

urlpatterns = [
    path("", upload_resume, name="upload"),
    path("review-ajax/", review_resume_ajax, name="review_ajax"),
]
