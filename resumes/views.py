from django.views.decorators.csrf import csrf_exempt
from .utils.prompt_builder import build_prompt
from .utils.pdf_parser import extract_text_from_pdf
from .utils.ai_client import get_resume_review
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ResumeUploadForm
import os

def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():
            resume = request.FILES["resume"]
            role = form.cleaned_data["role"]

            file_path = f"media/{resume.name}"
            with open(file_path, "wb+") as f:
                for chunk in resume.chunks():
                    f.write(chunk)

            resume_text = extract_text_from_pdf(file_path)
            prompt = build_prompt(resume_text, role)

            try:
                review = get_resume_review(prompt)
                print("REVIEW TYPE:", type(review))
            except Exception as e:
                print("AI ERROR:", e)
                return render(
                    request,
                    "resumes/upload.html",
                    {
                        "form": form,
                        "error": "AI service unavailable. Please try again."
                    }
                )

            # 🚫 Not a resume
            if not isinstance(review, dict) or not review.get("is_resume", False):
                return render(
                    request,
                    "resumes/review.html",
                    {
                        "review": review,
                        "role": role
                    }
                )

            # ✅ Valid resume (THIS WAS MISSING)
            print("VALID RESUME REVIEW:", review)
            return render(
                request,
                "resumes/review.html",
                {
                    "review": review,
                    "role": role
                }
            )

    else:
        form = ResumeUploadForm()

    return render(request, "resumes/upload.html", {"form": form})




# resumes/views.py  (replace the review_resume_ajax function)
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def review_resume_ajax(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    form = ResumeUploadForm(request.POST, request.FILES)

    if not form.is_valid():
        return JsonResponse({
            "error": "Invalid form data",
            "details": form.errors
        }, status=400)

    resume = request.FILES["resume"]
    role = form.cleaned_data["role"]

    file_path = f"media/{resume.name}"
    with open(file_path, "wb+") as f:
        for chunk in resume.chunks():
            f.write(chunk)

    resume_text = extract_text_from_pdf(file_path)
    prompt = build_prompt(resume_text, role)

    try:
        review = get_resume_review(prompt)
    except Exception:
        return JsonResponse({
            "error": "AI service unavailable"
        }, status=500)

    # 🔴 NOT A RESUME → FAILURE FRAGMENT
    if not isinstance(review, dict) or review.get("is_resume") is False:
        html = render_to_string(
            "resumes/failure_fragment.html",
            {"message": review.get("message", "Invalid resume file.")}
        )
        return JsonResponse({
            "html": html,
            "review": review
        })

    # 🟢 VALID RESUME → REVIEW FRAGMENT
    html = render_to_string(
        "resumes/review_fragment.html",
        {"review": review, "role": role}
    )

    return JsonResponse({
        "html": html,
        "review": review
    })