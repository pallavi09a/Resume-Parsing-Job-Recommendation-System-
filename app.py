from flask import Flask, render_template, request
import pickle
from PyPDF2 import PdfReader
import re
import string

app = Flask(__name__)

rf_classifier_categorization = pickle.load(open("models/rf_classifier_categorization.pkl", "rb"))
tfidf_vectorizer_categorization = pickle.load(open("models/tfidf_vectorizer_categorization.pkl", "rb"))
rf_classifier_job_recommendation = pickle.load(open("models/rf_classifier_job_recommendation.pkl", "rb"))
tfidf_vectorizer_job_recommendation = pickle.load(open("models/tfidf_vectorizer_job_recommendation.pkl", "rb"))


def cleanResume(txt):
    cleanText = re.sub(r'http\S+\s', ' ', txt)
    cleanText = re.sub(r'RT cc', ' ', cleanText)
    cleanText = re.sub(r'#\S+\s', ' ', cleanText)
    cleanText = re.sub(r'@\S+', ' ', cleanText)
    cleanText = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText


def predict_category(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_categorization.transform([resume_text])
    predicted_category = rf_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category


def job_recommendation(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_job_recommendation.transform([resume_text])
    recommended_job = rf_classifier_job_recommendation.predict(resume_tfidf)[0]
    return recommended_job


def pdf_to_text(file):
    reader = PdfReader(file)
    text = ''
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text


# ---------------- Resume Parsing ---------------- #

def extract_contact_number_from_resume(text):
    contact_number = None

    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number


def extract_email_from_resume(text):
    email = None

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email


def extract_skills_from_resume(text):
    skills_list = [
        "Python","Java","C","C++","C#","R","Go","Ruby","MATLAB","Perl","Swift","Kotlin","PHP","Scala",
        "TypeScript","HTML","CSS","JavaScript","Bootstrap","React","Angular","Vue.js","Node.js",
        "Express.js","Django","Flask","FastAPI","ASP.NET","REST API","SOAP","GraphQL",
        "SQL","MySQL","PostgreSQL","MongoDB","Oracle","SQLite","Redis","Cassandra","MariaDB",
        "AWS","Azure","Google Cloud","IBM Cloud","Heroku","Firebase",
        "Git","GitHub","GitLab","Docker","Kubernetes","Jenkins","Terraform","Linux","Shell Scripting",
        "Machine Learning","Deep Learning","NLP","Computer Vision","Data Analysis","TensorFlow",
        "PyTorch","Scikit-learn","Pandas","NumPy","Matplotlib","Seaborn",
        "Communication","Teamwork","Leadership","Problem Solving"
    ]

    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills


def extract_education_from_resume(text):
    education = []

    education_keywords = [
    "B.Tech", "BE", "M.Tech", "ME", "B.E.", "M.E.","Artificial Intelligence & Data Science", "B.Sc Engineering", "M.Sc Engineering", 
    "Diploma in Engineering", "Engineering Degree", "Computer Science", "Information Technology", 
    "Mechanical Engineering", "Civil Engineering", "Electrical Engineering", "Electronics Engineering", 
    "Chemical Engineering", "Aerospace Engineering", "Automobile Engineering", "Industrial Engineering",
    "BBA", "MBA", "PGDM", "B.Com", "M.Com", "Management Degree", "Business Administration", "Finance", 
    "Marketing", "Human Resources", "Operations Management", "Project Management", "Business Analytics", 
    "Supply Chain Management", "B.Sc", "M.Sc", "Physics", "Chemistry", "Mathematics", "Biology", "Software Developer", "Web Developer",
    "Environmental Science", "Data Science", "Statistics", "Analytics", "BA", "MA", "Journalism", 
    "Communication", "Psychology", "Sociology", "History", "English Literature", "Political Science", 
    "Philosophy", "AWS Certified Solutions Architect", "Azure Certification", "Google Cloud Certification", 
    "Cisco Certification", "CCNA", "CCNP", "Certified Ethical Hacker", "CEH", "Microsoft Certified", 
    "MCSE", "Scrum Master", "PMP", "Six Sigma", "Lean Six Sigma", "Diploma", "Certificate Course", "Management",
    "Vocational Training", "Internship", "Professional Training", "Short-term Course", "CFA", "CPA", "FRM", "CFP"
]


    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())

    return education


def extract_name_from_resume(text):
    name = None

    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()

    return name


@app.route("/")
def resume():
    return render_template("resume.html")


@app.route("/pred", methods=["POST"])
def pred():
    if 'resume' in request.files:
        file = request.files['resume']
        filename = file.filename

        if filename.endswith('.pdf'):
            text = pdf_to_text(file)
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return render_template("resume.html", message="Invalid file format.")

        predicted_category = predict_category(text)
        recommended_job = job_recommendation(text)
        phone = extract_contact_number_from_resume(text)
        email = extract_email_from_resume(text)
        extracted_skills = extract_skills_from_resume(text)
        extracted_education = extract_education_from_resume(text)
        name = extract_name_from_resume(text)

        return render_template(
            "resume.html",
            predicted_category=predicted_category,
            recommended_job=recommended_job,
            phone=phone,
            email=email,
            name=name,
            extracted_skills=extracted_skills,
            extracted_education=extracted_education
        )

    return render_template("resume.html", message="No resume file uploaded.")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=1919, debug=True)
