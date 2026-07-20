"""
prompts.py — all 8 system prompts used by analyzer.py.

Task 3 of the lab (Track A).
Study material references:
  §3.3 Schema-First Prompt Design
  §6.1 Extraction Prompts
  §6.2 Evaluation Prompts
  §6.3 Feedback-Only Principle

Every prompt must follow ICCO structure:
  Instruction  — what the model must do
  Context      — relevant background (rubric description, schema description)
  Constraints  — rules the model must not break
  Output       — the exact JSON schema expected

Every prompt (except OVERALL_SUMMARY_PROMPT) must end with:
  "Output ONLY a valid JSON object matching the schema above. No prose. No
  markdown fences. No commentary. Never rewrite or generate résumé content."

Temperature guidance (set in the ask_json() call in analyzer.py):
  Extraction prompts (RESUME_PROFILE, JD_PROFILE): 0.0
  Evaluation prompts (KEYWORD_MATCH, BULLET_QUALITY, JARGON, STRUCTURE, BACKGROUND_FIT): 0.2–0.3
  OVERALL_SUMMARY_PROMPT: 0.3
"""


# ---------------------------------------------------------------------------
# Extraction prompts
# ---------------------------------------------------------------------------

# Purpose: extract a structured candidate profile from plain résumé text.
# Input to ask_json(): system=RESUME_PROFILE_PROMPT, user="RÉSUMÉ TEXT:\n\n{text}"
# Expected output schema — all fields required; arrays may be empty:
# {
#   "name": "string",
#   "contact": {
#     "email": "string", "phone": "string", "linkedin": "string",
#     "github": "string", "portfolio": "string"
#   },
#   "summary": "string",
#   "education": [{"school": "string", "degree": "string",
#                  "graduation_date": "string", "courses": ["string"]}],
#   "projects":  [{"title": "string", "date": "string", "bullets": ["string"]}],
#   "experience":[{"title": "string", "company": "string",
#                  "date": "string", "bullets": ["string"]}],
#   "skills": {
#     "languages": ["string"], "frameworks": ["string"], "tools": ["string"],
#     "concepts": ["string"], "platforms": ["string"]
#   }
# }
RESUME_PROFILE_PROMPT = """
Instruction:
Extract a structured candidate profile from the provided résumé text.
Extract only information explicitly stated in the résumé.
Never infer, guess, or invent missing information.

Context:
The input is plain text extracted from a candidate's résumé.
The extracted profile will be used by later stages of a résumé and job description analysis pipeline for keyword matching, ATS evaluation, and diagnostic feedback.
Your task is only to organise the information into the required JSON structure.

Constraints:
- Extract only information explicitly present in the résumé.
- Never infer, guess, or fabricate missing information.
- Preserve wording where appropriate.
- If a field is missing, return an empty string or an empty array.
- Include every field in the schema even if empty.

Output:

{
  "name": "string",
  "contact": {
    "email": "string", "phone": "string", "linkedin": "string",
    "github": "string", "portfolio": "string"
  },
  "summary": "string",
  "education": [{"school": "string", "degree": "string",
                 "graduation_date": "string", "courses": ["string"]}],
  "projects":  [{"title": "string", "date": "string", "bullets": ["string"]}],
  "experience":[{"title": "string", "company": "string",
                 "date": "string", "bullets": ["string"]}],
  "skills": {
    "languages": ["string"], "frameworks": ["string"], "tools": ["string"],
    "concepts": ["string"], "platforms": ["string"]
  }
}

Output ONLY a valid JSON object matching the schema above.
No prose.
No markdown fences.
No commentary.
Never rewrite or generate résumé content.
"""


# Purpose: extract a structured JD profile from free-form job posting text.
# Input to ask_json(): system=JD_PROFILE_PROMPT, user="JOB DESCRIPTION TEXT:\n\n{text}"
# Expected output schema — all fields required; arrays may be empty:
# {
#   "job_title": "string",
#   "company": "string",
#   "location": "string",
#   "experience_level": "string",
#   "required_skills": ["string"],
#   "preferred_skills": ["string"],
#   "tools_technologies": ["string"],
#   "responsibilities": ["string"],
#   "soft_skills": ["string"],
#   "buzzwords": ["string"],
#   "deal_breakers": ["string"]
# }
JD_PROFILE_PROMPT = """
Instruction:
Extract a structured job description profile from the provided job description text.
Extract only information explicitly stated in the job description.
Never infer, guess, or invent missing information.

Context:
The input is plain text extracted from a job description.
The extracted profile will be used by later stages of a résumé and job description analysis pipeline for keyword matching, ATS evaluation, and diagnostic feedback.
Your task is only to organise the information into the required JSON structure.

Constraints:
- Extract only information explicitly present in the job description.
- Never infer, guess, or fabricate missing information.
- Preserve wording where appropriate.
- Return every field defined in the schema, even if its value is empty.
- If a field is missing, return an empty string or an empty array.

- required_skills must contain individual skills, programming languages, frameworks, tools, platforms, methodologies, or technical concepts rather than complete requirement sentences.

- preferred_skills must also contain individual skill names rather than complete sentences.

- tools_technologies must contain only the names of technologies, languages, frameworks, tools, platforms, software, or protocols mentioned in the job description.

- responsibilities should contain the complete responsibility statements exactly as described in the job description.

- When a requirement sentence contains multiple skills, split them into separate array elements.

- Do not include introductory phrases such as:
  - "Experience with"
  - "Knowledge of"
  - "Familiarity with"
  - "Proficiency in"
  - "Understanding of"

Examples:

"Proficiency in Python, Go, or C++"
→ ["Python", "Go", "C++"]

"Experience with Linux operating systems and Bash scripting"
→ ["Linux", "Bash"]

"Knowledge of React, Node.js, Express, and MongoDB"
→ ["React", "Node.js", "Express", "MongoDB"]

"Experience with Docker, Kubernetes, and AWS"
→ ["Docker", "Kubernetes", "AWS"]

Apply these rules consistently for any programming language, framework, tool, platform, protocol, methodology, software, cloud service, certification, or technical concept mentioned in the job description.

Output:

{
  "job_title": "string",
  "company": "string",
  "location": "string",
  "experience_level": "string",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "tools_technologies": ["string"],
  "responsibilities": ["string"],
  "soft_skills": ["string"],
  "buzzwords": ["string"],
  "deal_breakers": ["string"]
}

Output ONLY a valid JSON object matching the schema above.
No prose.
No markdown fences.
No commentary.
Never rewrite or generate résumé content.
"""


# ---------------------------------------------------------------------------
# Evaluation prompts
# ---------------------------------------------------------------------------

# Purpose: compare résumé keywords against JD requirements; produce a score.
# Input to ask_json():
#   system=KEYWORD_MATCH_PROMPT
#   user="RÉSUMÉ PROFILE:\n{json}\n\nJD PROFILE:\n{json}"
# Expected output schema:
# {
#   "present": [{"keyword": "string", "category": "language|framework|tool|concept|soft_skill|buzzword",
#                "found_in": "summary|projects|experience|education|skills", "exact_match": true}],
#   "missing": [{"keyword": "string", "category": "...", "importance": "required|preferred",
#                "suggested_section": "skills|projects|experience|summary",
#                "why_it_matters": "string (25 words max — diagnostic only)"}],
#   "keyword_match_score": 0
# }
# Scoring formula: 100 × (required_skills found in résumé) / max(1, total required_skills)
# IMPORTANT: the résumé and JD profiles are always provided in full, even when
# they share zero keywords — that is a normal, valid input, not a missing one.
# The model must still return the schema (an empty "present" array is a
# correct result) rather than asking for clarification or claiming no résumé
# was given. Small/local models are especially prone to breaking character on
# a total-mismatch input, so state this constraint explicitly.
KEYWORD_MATCH_PROMPT = """
Instruction:
Compare the provided résumé profile against the provided job description profile.
Identify which required and preferred keywords are present in the résumé and which are missing.
Evaluate the overall keyword match based only on the supplied profiles.

Context:
The résumé profile and job description profile have already been extracted into structured JSON objects.
The goal is to assess how well the candidate's skills and experience align with the job requirements for ATS-style keyword matching.
It is valid for the résumé and job description to have zero matching keywords.
Even if no keywords match, you must still complete the evaluation and return the required JSON structure.

Constraints:
- Use only the information provided in the résumé profile and job description profile.
- Never infer, guess, or invent keywords that are not present.
- Never ask for clarification or state that the résumé or job description is missing.
- The "present" array may be empty if there are no matching keywords.
- The "missing" array should include keywords required or preferred by the job description that do not appear in the résumé.
- "why_it_matters" must be diagnostic only and must not rewrite résumé content.
- Compute the keyword_match_score using: 100 * (required_skills found in résumé) / max(1, total required_skills)

Output:

{
  "present": [{"keyword": "string", "category": "language|framework|tool|concept|soft_skill|buzzword",
               "found_in": "summary|projects|experience|education|skills", "exact_match": true}],
  "missing": [{"keyword": "string", "category": "...", "importance": "required|preferred",
               "suggested_section": "skills|projects|experience|summary",
               "why_it_matters": "string (25 words max — diagnostic only)"}],
  "keyword_match_score": 0
}

Output ONLY a valid JSON object matching the schema above.
No prose.
No markdown fences.
No commentary.
Never rewrite or generate résumé content.
"""


# Purpose: score each résumé bullet against the Action → Technology → Impact rubric.
# Input to ask_json(): system=BULLET_QUALITY_PROMPT, user="RÉSUMÉ PROFILE:\n{json}"
# Expected output schema:
# {
#   "bullets": [{"source": "projects|experience", "parent_title": "string",
#                "bullet_text": "string (verbatim)", "has_action_verb": true,
#                "has_specific_technology": true, "has_measurable_impact": false,
#                "level": "L1_OK|L2_BETTER|L3_BEST",
#                "what_is_missing": "string (20 words max — diagnose only)"}],
#   "bullet_quality_avg": 0
# }
# Scoring formula: round(100 × sum(level_score) / (3 × count)) where L1=1, L2=2, L3=3
# IMPORTANT: embed the Action→Technology→Impact rubric verbatim inside this prompt,
# including the L1/L2/L3 reference level examples. This is a well-known, general
# résumé-writing framework — no external reference document needed.
BULLET_QUALITY_PROMPT = """
Instruction:
Evaluate every résumé bullet in the provided résumé profile using the Action → Technology → Impact (ATI) rubric.
Assess each bullet independently and assign the appropriate quality level.
Produce only diagnostic feedback without rewriting any résumé content.

Context:
A strong résumé bullet clearly describes:
- the action performed,
- the specific technology, tool, framework, or method used,
- and the measurable outcome or impact achieved.

Use the following Action → Technology → Impact rubric.

L1_OK (Action Only)
- Describes what the candidate did.
- Contains an action verb.
- Does not mention a specific technology or measurable outcome.

Example:
"Developed a web application."

L2_BETTER (Action + Technology)
- Describes what the candidate did.
- Mentions the specific technology, framework, language, or tool used.
- Does not include a measurable result.

Example:
"Developed a web application using React and Flask."

L3_BEST (Action + Technology + Impact)
- Describes what the candidate did.
- Mentions the specific technology, framework, language, or tool used.
- Includes a measurable outcome, improvement, or business impact.

Example:
"Developed a React and Flask web application that reduced page load time by 35%."

Evaluate every bullet using this rubric.

Constraints:
- Evaluate only bullets contained in the provided résumé profile.
- Do not rewrite or improve any bullet.
- Preserve each bullet exactly as written.
- Determine whether each bullet contains:
  - an action verb,
  - a specific technology,
  - a measurable impact.
- Assign exactly one level:
  - L1_OK
  - L2_BETTER
  - L3_BEST
- The "what_is_missing" field must be diagnostic only.
- Do not suggest rewritten bullets.
- If there are no bullets, return an empty array and a score of 0.
- Compute bullet_quality_avg using:
  round(100 * sum(level_score) / (3 * bullet_count))
  where:
  L1_OK = 1
  L2_BETTER = 2
  L3_BEST = 3

Output:

{
  "bullets": [{"source": "projects|experience", "parent_title": "string",
               "bullet_text": "string (verbatim)", "has_action_verb": true,
               "has_specific_technology": true, "has_measurable_impact": false,
               "level": "L1_OK|L2_BETTER|L3_BEST",
               "what_is_missing": "string (20 words max — diagnose only)"}],
  "bullet_quality_avg": 0
}

Output ONLY a valid JSON object matching the schema above.
No prose.
No markdown fences.
No commentary.
Never rewrite or generate résumé content.
"""


# Purpose: detect résumé terminology that is a likely semantic match for JD
#          terminology but would not literally keyword-match an ATS scan.
# Input to ask_json():
#   system=JARGON_AUDIT_PROMPT
#   user="RÉSUMÉ PROFILE:\n{json}\n\nJD PROFILE:\n{json}"
# Expected output schema:
# {
#   "flags": [{"bullet_text": "string (verbatim)", "term_used": "string",
#              "suggested_translation": "string", "severity": "low|medium|high"}],
#   "jargon_score": 0
# }
# No static table: the model compares résumé text against JD text dynamically —
# a real ATS/recruiter tool does semantic matching, not a hand-maintained dictionary.
# Severity rules: high if the JD uses no equivalent language at all; medium if
# partial overlap; low if the JD already uses matching or adjacent terminology.
# Scoring formula: max(0, 100 - 10*high_count - 5*medium_count - 2*low_count)
JARGON_AUDIT_PROMPT = """
Instruction:
Compare the terminology used in the résumé profile with the terminology used in the job description profile.
Identify résumé terms that are likely to describe the same concepts as the job description but use different wording that may reduce literal ATS keyword matching.
Evaluate the severity of each terminology difference and calculate an overall jargon score.

Context:
Modern ATS systems and recruiters rely on both exact keyword matching and semantic understanding.
Candidates often describe the same skill, technology, or responsibility using different terminology than the job description.
Your task is to identify terminology differences that could reduce keyword matching while avoiding false positives.
Compare the résumé profile and job description profile dynamically using the information provided.
Do not rely on any predefined synonym list or static translation table.

Severity Guidelines:
- High:
  The résumé uses terminology that has no clear equivalent wording used in the job description and is likely to reduce ATS keyword matching.

- Medium:
  The résumé partially overlaps with the terminology used in the job description but could benefit from closer wording.

- Low:
  The résumé terminology already closely matches or uses adjacent wording found in the job description.

Constraints:
- Compare only the supplied résumé profile and job description profile.
- Never invent terminology that does not appear in either profile.
- Do not rewrite or improve résumé bullets.
- Preserve bullet_text exactly as provided.
- suggested_translation must describe the equivalent job-description terminology only.
- suggested_translation is diagnostic only and must not become a rewritten résumé bullet.
- Return an empty flags array if no terminology differences are found.
- Compute the jargon_score using:
  max(0, 100 - 10 * high_count - 5 * medium_count - 2 * low_count)

Output:

{
  "flags": [{"bullet_text": "string (verbatim)", "term_used": "string",
             "suggested_translation": "string", "severity": "low|medium|high"}],
  "jargon_score": 0
}

Output ONLY a valid JSON object matching the schema above.
No prose.
No markdown fences.
No commentary.
Never rewrite or generate résumé content.
"""


# Purpose: audit general ATS-parseability formatting.
# Input to ask_json(): system=STRUCTURE_AUDIT_PROMPT, user="RÉSUMÉ TEXT:\n\n{text}"
# Expected output schema:
# {
#   "page_count_estimate": 1,
#   "single_column_likely": true,
#   "section_headings_present": ["string"],
#   "section_headings_missing": ["string"],
#   "reverse_chronological_likely": true,
#   "contact_info_at_top": true,
#   "length_appropriate": true,
#   "no_images_or_graphics": true,
#   "ats_red_flags": [{"issue": "string", "evidence": "string"}],
#   "structure_score": 0
# }
# IMPORTANT: embed general ATS-parseability rules verbatim inside this prompt:
# single-column layout, standard section headers, reverse-chronological order,
# appropriate length, contact info placement, no images/graphics. These are
# well-known conventions — no external reference document needed.
STRUCTURE_AUDIT_PROMPT = """
Instruction:
Evaluate the résumé text for general ATS parseability and formatting.
Assess whether the résumé follows common ATS-friendly structure and identify any formatting issues that may reduce successful parsing.
Provide only diagnostic feedback.

Context:
Most Applicant Tracking Systems (ATS) perform best when a résumé follows standard formatting conventions.
Evaluate the résumé using the following ATS parseability guidelines:

- Single-column layout
- Standard section headings (such as Summary, Education, Experience, Projects, Skills)
- Reverse-chronological order for education and experience
- Appropriate résumé length
- Contact information placed near the top of the résumé
- No images, graphics, tables, icons, text boxes, or decorative elements that may interfere with parsing

Use only the provided résumé text when making your assessment.

Constraints:
- Evaluate only information present in the résumé text.
- Never infer formatting features that cannot reasonably be determined from the text.
- Report only observable ATS issues.
- If no issues are found, return an empty ats_red_flags array.
- Do not rewrite or improve the résumé.
- Compute structure_score (0-100) by starting at 0 and adding 20 points for each of the following that is evaluated as true:
  1. single_column_likely
  2. reverse_chronological_likely
  3. contact_info_at_top
  4. length_appropriate
  5. no_images_or_graphics

Output:

{
  "page_count_estimate": 1,
  "single_column_likely": true,
  "section_headings_present": ["string"],
  "section_headings_missing": ["string"],
  "reverse_chronological_likely": true,
  "contact_info_at_top": true,
  "length_appropriate": true,
  "no_images_or_graphics": true,
  "ats_red_flags": [{"issue": "string", "evidence": "string"}],
  "structure_score": 0
}

Output ONLY a valid JSON object matching the schema above.
No prose.
No markdown fences.
No commentary.
Never rewrite or generate résumé content.
"""


# Purpose: assess how well the candidate's stated education/experience background
# plausibly aligns with what this role is asking for — using only data already
# extracted into resume_profile and jd_profile (no external degree code needed).
# Input to ask_json():
#   system=BACKGROUND_FIT_PROMPT
#   user="RÉSUMÉ PROFILE:\n{json}\n\nJD PROFILE:\n{json}"
# Expected output schema:
# {
#   "candidate_background_summary": "string (1–2 sentences)",
#   "role_requirements_summary": "string (1–2 sentences)",
#   "alignment_commentary": "string (2–3 sentences — diagnostic only)",
#   "background_fit_score": 0
# }
BACKGROUND_FIT_PROMPT = """
Instruction:
Evaluate how well the candidate's educational background and professional experience align with the requirements of the job description.
Assess the overall suitability using only the information contained in the provided résumé profile and job description profile.
Provide diagnostic feedback only.

Context:
The résumé profile contains the candidate's education, projects, work experience, and skills.
The job description profile contains the role requirements, required skills, preferred skills, responsibilities, and experience level.
Your task is to compare these structured profiles and assess how well the candidate's background matches the role.
Use only the extracted profile data provided.
Do not rely on external knowledge, assumptions, degree classifications, or industry-specific requirements.

Constraints:
- Evaluate only the information present in the provided résumé profile and job description profile.
- Never infer or invent qualifications, experience, or skills.
- Do not assume a candidate is qualified or unqualified based on information that is not explicitly provided.
- candidate_background_summary must summarise only the candidate's stated background.
- role_requirements_summary must summarise only the stated job requirements.
- alignment_commentary must explain the strengths and gaps between the candidate and the role.
- alignment_commentary must be diagnostic only and must not rewrite or improve the résumé.
- Compute background_fit_score (0-100) using this strict rubric:
  - 0-25: Completely unrelated background.
  - 26-50: Weak alignment (missing major required experience or education).
  - 51-75: Moderate alignment (meets basic requirements but lacks preferred depth).
  - 76-100: Strong alignment (highly relevant experience and education).

Output:

{
  "candidate_background_summary": "string (1-2 sentences)",
  "role_requirements_summary": "string (1-2 sentences)",
  "alignment_commentary": "string (2-3 sentences - diagnostic only)",
  "background_fit_score": 0
}

Output ONLY a valid JSON object matching the schema above.
No prose.
No markdown fences.
No commentary.
Never rewrite or generate résumé content.
"""


# ---------------------------------------------------------------------------
# Synthesis prompt
# ---------------------------------------------------------------------------

# Purpose: produce a 3-bullet plain Markdown executive summary from the full report.
# Input to ask_text(): system=OVERALL_SUMMARY_PROMPT, user="ANALYSIS REPORT:\n{json}"
# Returns: plain Markdown string (not JSON).
# NOTE: this prompt does NOT need the JSON output constraint line.
#       It also does NOT need a JSON schema — ask_text() is used, not ask_json().
# The summary must be diagnostic only — no rewrites, no generated résumé content.
OVERALL_SUMMARY_PROMPT = """
Instruction:
Summarise the completed résumé analysis report into three concise executive summary bullet points.
Highlight the candidate's overall ATS readiness, the strongest areas of alignment, and the most significant improvement opportunities.
Provide diagnostic feedback only.

Context:
The input is a completed résumé analysis report containing the extracted résumé profile, extracted job description profile, keyword match evaluation, bullet quality evaluation, jargon audit, ATS structure audit, background fit assessment, and overall score.
Your task is to produce a concise executive summary that helps the user quickly understand the overall results.

Constraints:
- Produce exactly three Markdown bullet points.
- Each bullet should be concise and easy to understand.
- Summarise only the information contained in the analysis report.
- Do not invent new findings or recommendations.
- Do not rewrite or improve the résumé.
- Do not generate new résumé content.
- Keep the tone objective, professional, and diagnostic.

Output:
Return exactly three Markdown bullet points.
Do not return JSON.
Do not include headings, introductions, conclusions, explanations, or commentary.
"""

# ---------------------------------------------------------------------------
# Degree prompt
# ---------------------------------------------------------------------------

DEGREE_ALIGNMENT_PROMPT = """\
You are a degree-alignment checker. You are given a JD profile JSON and the
student's degree program code. You check whether the JD job title is on the
suggested-titles list for the student's degree.

Degree-Aligned Job Title Lists
===============================
RTIS (Real-Time Interactive Simulation):
  Game Engine Developer, Systems Engineer, Site Reliability Engineer (SRE),
  DevOps Engineer, AI/ML Engineer, Data Analyst / Data Scientist,
  Full Stack Developer, Cybersecurity Engineer, Simulation Engineer,
  Graphics Programmer, Technical Product Manager, Technical Project Manager

IMGD (Interactive Media & Game Development):
  Game Developer, Systems Engineer, Full Stack Developer, Data Engineer,
  Infrastructure Engineer, DevOps Engineer, Cybersecurity Engineer,
  AI/ML Engineer, Technical Designer, Technical Artist,
  Gameplay Programmer, Tools Engineer,
  Technical Product Manager, Technical Project Manager

UXGD (User Experience & Game Design):
  App Developer, UI/UX Designer, Product Designer, Product Manager,
  Product Operations Manager, Project Manager, Marketing & Design Specialist,
  Process Architect, Technical Designer, Technical Artist,
  UX Researcher, UX Engineer

BFA (Digital Art and Animation):
  Technical Artist, UI/UX Designer, Creative Designer, Unreal Engine Artist,
  3D Graphic Artist, Production Assistant, Project Manager, Project Operations

Matching rule:
- title_on_suggested_list is true if the JD title matches an entry exactly OR
  is a clear variant (e.g. "Junior Systems Engineer" matches "Systems Engineer").
- If false, set degree_alignment_score to 50-70 with fit_commentary explaining
  the mismatch. Never invent a match.

JSON schema:

{
  "student_degree": "string",
  "jd_title": "string",
  "title_on_suggested_list": true,
  "matched_against": "string",
  "fit_commentary": "string (40 words or fewer)",
  "degree_alignment_score": 100
}

Output ONLY a valid JSON object matching the schema above. No prose. No
markdown fences. Never rewrite or generate résumé content.
"""