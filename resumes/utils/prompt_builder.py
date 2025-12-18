from .role_profiles import ROLE_PROFILES


def build_prompt(resume_text, role):
  profile = ROLE_PROFILES.get(role)
  if not profile:
    raise ValueError(f"Unsupported role: {role}")
  return f"""
You are a senior technical recruiter and hiring engineer.

YOUR FIRST TASK (MANDATORY):
Determine whether the provided text is any kind of resume or CV.

IF THE TEXT IS NOT A RESUME:
- Return ONLY the following JSON
- Do NOT include any extra keys
- Do NOT include explanations outside JSON

{{
  "is_resume": false,
  "message": "The uploaded file could not be identified as a valid resume."
}}

IF THE TEXT IS A RESUME:
- Set "is_resume": true
- Return the FULL analysis JSON described below
- Base all feedback strictly on the resume text
- Do NOT invent experience
- Be concise, recruiter-like, and practical

ROLE CONTEXT:
Target role: {role.upper()}
Core expectations: {profile['core']}
Bonus expectations: {profile['bonus']}

STRICT RULES (FOR BOTH CASES):
- Output ONLY valid JSON
- No markdown
- No explanations outside JSON
- No partial schemas

ATS & CLARITY REQUIREMENTS:
- For every ATS or clarity issue you identify, include ONE concrete example from the resume text
- Combine the issue and its example into a single sentence
- Do NOT list generic advice without evidence

FULL RESUME ANALYSIS JSON FORMAT (ONLY IF is_resume = true):

{{
  "is_resume": true,
  "summary": {{
    "strengths": "",
    "level_estimate": "",
    "role_fit": ""
  }},
  "skills": {{
    "strong": [],
    "missing_or_weak": [],
    "should_highlight": []
  }},
  "projects_experience": {{
    "strong_points": "",
    "weak_points": "",
    "sample_rewrite": ""
  }},
  "ats_clarity": {{
    "issues": [],
    "improvements": []
  }},
  "scores": {{
    "role_fit": "",
    "clarity": "",
    "impact": "",
    "overall": ""
  }},
  "action_items": []
}}

TEXT TO ANALYZE:
{resume_text}
"""
