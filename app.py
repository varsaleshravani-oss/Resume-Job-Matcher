
import streamlit as st
import re
from io import BytesIO

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# 1. Page Settings
# -----------------------------
st.set_page_config(
    page_title="Resume–Job Matcher",
    page_icon="📄",
    layout="centered"
)


# -----------------------------
# 2. Application Title
# -----------------------------
st.title("📄 Resume–Job Description Matcher")

st.write(
    "Upload your resume and paste a job description "
    "to check text similarity and skill coverage."
)


# -----------------------------
# 3. Resume Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


# -----------------------------
# 4. Job Description Input
# -----------------------------
job_description = st.text_area(
    "Paste the Job Description",
    height=200
)


# -----------------------------
# 5. Skills List
# -----------------------------
skills = [
    "Python",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "TensorFlow",
    "PyTorch",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Excel",
    "Communication",
    "Problem Solving"
]


# -----------------------------
# 6. Skill Detection Function
# -----------------------------
def find_skills(text, skills):
    found_skills = []

    for skill in skills:
        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


# -----------------------------
# 7. Check Match Button
# -----------------------------
if st.button("Check Match", type="primary"):

    if uploaded_file is not None and job_description.strip():

        try:
            # Read PDF and extract text
            reader = PdfReader(uploaded_file)
            resume_text = ""

            for page in reader.pages:
                resume_text += page.extract_text() or ""

            # Check for readable text
            if not resume_text.strip():
                st.error(
                    "No readable text found in the PDF. "
                    "Please upload a text-based resume."
                )
                st.stop()

            # -----------------------------
            # 8. Calculate Text Similarity
            # -----------------------------
            documents = [
                resume_text,
                job_description
            ]

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(documents)

            similarity = cosine_similarity(
                tfidf_matrix[0],
                tfidf_matrix[1]
            )[0][0]

            # -----------------------------
            # 9. Detect Skills
            # -----------------------------
            resume_skills = find_skills(
                resume_text, skills
            )

            job_skills = find_skills(
                job_description, skills
            )

            matching_skills = [
                skill for skill in job_skills
                if skill in resume_skills
            ]

            missing_skills = [
                skill for skill in job_skills
                if skill not in resume_skills
            ]

            # -----------------------------
            # 10. Calculate Skill Coverage
            # -----------------------------
            if job_skills:
                skill_match = (
                    len(matching_skills) / len(job_skills)
                ) * 100
            else:
                skill_match = 0

            # -----------------------------
            # 11. Display Match Report
            # -----------------------------
            st.subheader("📊 Match Report")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Text Similarity",
                    f"{similarity * 100:.2f}%"
                )

            with col2:
                if job_skills:
                    st.metric(
                        "Job Skill Coverage",
                        f"{skill_match:.0f}%"
                    )
                else:
                    st.metric(
                        "Job Skill Coverage",
                        "N/A"
                    )

            # Display skill coverage progress
            if job_skills:
                st.progress(
                    float(skill_match / 100)
                )

                st.write(
                    f"You have {len(matching_skills)} out of "
                    f"{len(job_skills)} detected required skills."
                )
            else:
                st.info(
                    "No predefined skills detected in the "
                    "job description."
                )

            # -----------------------------
            # 12. Matching Skills
            # -----------------------------
            st.subheader("✅ Matching Skills")

            if matching_skills:
                st.write(", ".join(matching_skills))
            else:
                st.write("No matching skills detected.")

            # -----------------------------
            # 13. Missing Skills
            # -----------------------------
            st.subheader("📚 Skills to Improve")

            if missing_skills:
                st.write(", ".join(missing_skills))
            else:
                st.write(
                    "All detected job-description skills "
                    "were found in your resume."
                )

            # -----------------------------
            # 14. Resume Skills
            # -----------------------------
            st.subheader("📝 Skills Found in Your Resume")

            if resume_skills:
                st.write(", ".join(resume_skills))
            else:
                st.write("No predefined skills detected.")

            # -----------------------------
            # 15. Generate PDF Report
            # -----------------------------
            pdf_buffer = BytesIO()

            pdf = canvas.Canvas(
                pdf_buffer,
                pagesize=A4
            )

            width, height = A4
            y = height - 50

            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawString(
                50, y,
                "Resume-Job Match Report"
            )

            y -= 40
            pdf.setFont("Helvetica", 12)

            pdf.drawString(
                50, y,
                f"Text Similarity: {similarity * 100:.2f}%"
            )

            y -= 25

            if job_skills:
                pdf.drawString(
                    50, y,
                    f"Job Skill Coverage: {skill_match:.0f}%"
                )
                y -= 30

            # Matching skills section
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(
                50, y,
                "Matching Skills:"
            )

            y -= 20
            pdf.setFont("Helvetica", 11)

            for skill in matching_skills:
                if y < 50:
                    pdf.showPage()
                    y = height - 50
                    pdf.setFont("Helvetica", 11)

                pdf.drawString(
                    60, y,
                    f"- {skill}"
                )
                y -= 18

            # Missing skills section
            y -= 10

            if y < 70:
                pdf.showPage()
                y = height - 50

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(
                50, y,
                "Skills to Improve:"
            )

            y -= 20
            pdf.setFont("Helvetica", 11)

            if missing_skills:
                for skill in missing_skills:
                    if y < 50:
                        pdf.showPage()
                        y = height - 50
                        pdf.setFont("Helvetica", 11)

                    pdf.drawString(
                        60, y,
                        f"- {skill}"
                    )
                    y -= 18
            else:
                pdf.drawString(
                    60, y,
                    "No detected skills missing."
                )
                y -= 18

            # Resume skills section
            y -= 10

            if y < 70:
                pdf.showPage()
                y = height - 50

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(
                50, y,
                "Skills Found in Resume:"
            )

            y -= 20
            pdf.setFont("Helvetica", 11)

            for skill in resume_skills:
                if y < 50:
                    pdf.showPage()
                    y = height - 50
                    pdf.setFont("Helvetica", 11)

                pdf.drawString(
                    60, y,
                    f"- {skill}"
                )
                y -= 18

            # Disclaimer
            y -= 15

            if y < 50:
                pdf.showPage()
                y = height - 50

            pdf.setFont("Helvetica-Oblique", 9)
            pdf.drawString(
                50, y,
                "Scores are not hiring probabilities."
            )

            pdf.save()
            pdf_buffer.seek(0)

            # -----------------------------
            # 16. Download PDF Button
            # -----------------------------
            st.download_button(
                label="📥 Download Match Report (PDF)",
                data=pdf_buffer.getvalue(),
                file_name="resume_match_report.pdf",
                mime="application/pdf"
            )

            # Disclaimer on application
            st.caption(
                "Text similarity and skill coverage are not "
                "hiring probabilities. Results depend on the "
                "predefined skill list and PDF text extraction."
            )

        except Exception as error:
            st.error(
                f"Something went wrong while processing "
                f"your resume: {error}"
            )

    else:
        st.warning(
            "Please upload a PDF resume and enter a job description."
        )
