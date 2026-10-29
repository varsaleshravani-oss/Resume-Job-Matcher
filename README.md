# Resume–Job Description Matcher Using NLP

## Project Overview
The Resume–Job Description Matcher is a Python-based web application that compares a candidate's resume with a job description. It calculates text similarity, identifies matching skills, and highlights skills that may be missing from the resume.

## Features
- Upload resumes in PDF format.
- Extract resume text using PyPDF.
- Calculate text similarity using TF-IDF and cosine similarity.
- Identify matching and missing skills using keyword detection.
- Calculate job skill coverage percentage.
- Download a match report as a PDF.

## Technologies Used
- Python
- Streamlit
- Scikit-learn
- PyPDF
- ReportLab
- Natural Language Processing (NLP) techniques

## Installation

1. Install Python.
2. Download or clone this repository.
3. Open the project folder in the terminal.
4. Install the required libraries:

   `python -m pip install -r requirements.txt`

5. Run the application:

   `python -m streamlit run app.py`

6. Open the local URL displayed in the terminal.

## How to Use
1. Upload a text-based PDF resume.
2. Paste the job description.
3. Click **Check Match**.
4. Review the text similarity, skill coverage, matching skills, and skills to improve.
5. Download the match report as a PDF.

## How It Works
- **PDF Extraction:** Extracts readable text from the uploaded resume.
- **TF-IDF:** Converts resume and job-description text into numerical features.
- **Cosine Similarity:** Measures similarity between the two text documents.
- **Skill Detection:** Searches for predefined skill keywords.
- **PDF Report:** Generates a downloadable summary of the results.

## Limitations
- Skill detection uses a predefined list of keywords.
- Scanned PDFs without readable text are not supported.
- Similarity and skill coverage scores are not hiring probabilities.
- Results depend on the extracted text and predefined skills.

## Future Improvements
- Add more technical skills and synonyms.
- Improve the user interface.
- Support additional resume formats.
- Add more advanced semantic text matching.

## Author
Shravani Varsale

B.Tech Artificial Intelligence