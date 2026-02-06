# Resume Parsing & Job Recommendation System

```bash
This Resume Screening AI system automatically analyzes resumes uploaded in PDF or TXT format. It predicts the candidate’s job category, recommends suitable roles, and extracts key information such as name, skills, education, email, and contact number.
```

# How to run code ?

### Step 1: Create and Activate Virtual Environment

```bash
python -m venv resumeparsing
source resumeparsing/Scripts/activate

```

### Step 2: Install Required Libraries

```bash
pip install flask scikit-learn PyPDF2 pdfminer.six numpy pandas
```

### Step 3: Run the Flask Application
```bash
python app.py
```

### Step 4: Open in Browser
```bash
http://127.0.0.1:1919
```






# Techniques & Technologies Used

### 1. Natural Language Processing (NLP)
- Text cleaning using Regular Expressions (Regex)
- Removal of URLs, special characters, and extra spaces
- Resume text normalization

### 2. Feature Extraction
- TF-IDF (Term Frequency–Inverse Document Frequency)
- Converts resume text into numerical vectors

### 3. Machine Learning Algorithms
- Random Forest Classifier
  - Resume Categorization
  - Job Recommendation
- Models trained on labeled resume data
- Models stored using Pickle

### 4. Resume Parsing Techniques
- Regex-based extraction for:
  - Name
  - Email ID
  - Phone Number
  - Skills
  - Education
- Keyword-based matching for skills and education

### 5. Web Framework
- Flask (Python)
  - Handles resume upload
  - Processes PDF/TXT files
  - Displays results on UI

---

## Tech Stack
- Programming Language: Python
- Web Framework: Flask
- Machine Learning: Scikit-learn
- NLP: Regex, TF-IDF
- PDF Processing: PyPDF2
- Frontend: HTML, CSS, Jinja2
- Model Storage: Pickle

