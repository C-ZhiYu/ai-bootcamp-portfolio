import streamlit as st
from dotenv import load_dotenv

from parse import read_resume_pdf
from analyzer import (
    extract_resume_profile, extract_jd_profile, analyse_keyword_match,
    analyse_bullets, analyse_jargon, analyse_structure,
    analyse_degree_alignment, summarise_overall, compute_overall_score,
)

load_dotenv()
VALID_DEGREES = ["RTIS", "IMGD", "UXGD", "BFA"]

ATS_PASS_THRESHOLD = 60

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=250)
degree = st.selectbox("Select Degree", VALID_DEGREES)
run = st.button("Analyze Resume")

if run:
    if not resume_file or not jd_text:
        st.error("Please upload resume and paste job description.")
        st.stop()

    # 2: Load Resume
    with st.spinner("Analyzing resume against job description..."):
        resume_text = read_resume_pdf(resume_file)

        # 3: Extract Structure profiles
        resume_profile = extract_resume_profile(resume_text)
        jd_profile = extract_jd_profile(jd_text)

        # 4: Run the 5 evaluations
        keyword_match = analyse_keyword_match(resume_profile, jd_profile)
        bullets = analyse_bullets(resume_profile)
        jargon = analyse_jargon(resume_profile, jd_profile)
        structure = analyse_structure(resume_text)

        degree_alignment = analyse_degree_alignment(jd_profile, degree)
        
        # 9: Assemble the report dict
        report: dict = {
            "resume_profile": resume_profile,
            "jd_profile": jd_profile,
            "keyword_match": keyword_match,
            "bullets": bullets,
            "jargon": jargon,
            "structure": structure,
            "degree_alignment": degree_alignment,
        }

        # Compute overall score and add to report
        overall_score = compute_overall_score(report)
        report["overall_score"] = overall_score
        passes_ats_threshold = overall_score >= ATS_PASS_THRESHOLD

        report["passes_ats_threshold"] = passes_ats_threshold
        summary = summarise_overall(report)
        report["summary"] = summary

        st.subheader("Analysis Results")
        if passes_ats_threshold:
                st.success(f"**Verdict:** PASS (Score: {overall_score})")
        else:
            st.error(f"**Verdict:** FAIL (Score: {overall_score})")

        st.markdown("### Summary")
        st.markdown(summary) 

        st.markdown("---")
        st.markdown("### 🎓 Degree Alignment")

        # Extract the values from the dictionary
        alignment_score = degree_alignment.get("degree_alignment_score", 0)
        matched_title = degree_alignment.get("matched_against", "N/A")
        commentary = degree_alignment.get("fit_commentary", "")
        is_on_list = degree_alignment.get("title_on_suggested_list", False)

        # Create a mini dashboard for the degree
        deg_col1, deg_col2 = st.columns([1, 3])

        with deg_col1:
            st.metric(label="Alignment Score", value=f"{alignment_score}/100")

        with deg_col2:
            st.markdown(f"**Matched Against:** `{matched_title}`")
            
            # Use color-coded callouts based on the boolean flag or score
            if is_on_list:
                st.success(f"**Great Fit:** The target role is a highly recommended path for {degree} graduates.")
            else:
                st.warning(f"**Mismatch Detected:** {commentary}")