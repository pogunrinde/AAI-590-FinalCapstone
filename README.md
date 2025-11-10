# AAI-590-FinalCapstone
Intelligent NLP System for Extracting and Structuring Key Information from FDA Regulatory.

FDA Regulatory Data Analysis & Modeling
University of San Diego — Class Project

Project Overview
This project explores how publicly available FDA data can be used to analyze, model, and understand regulatory activities related to drugs, biologics, and medical devices.
The primary goal is to clean, structure, and model FDA datasets to identify relationships between regulations, recalls, and adverse events — and to explore whether machine learning techniques can predict which regulations may apply to a given product or study type.
This work aims to build a foundation for an intelligent search and recommendation system that links study requirements or product features to relevant FDA regulations and guidance documents.

Objectives
Collect and preprocess FDA data from official open data sources.
Apply text processing (tokenization, NER, and POS tagging) to clean regulatory documents.
Analyze recalls and adverse event data to uncover common patterns.
Explore unsupervised and supervised machine learning models to connect regulatory topics with product or study categories.
Visualize and summarize relationships between regulation types and product outcomes.

Datasets
We use open FDA datasets from the OpenFDA API, including:
Regulatory and Guidance Documents (Drugs, Devices, Biologics)
Recalls and Enforcement Reports
Adverse Events Data
All data are publicly available and used strictly for academic and non-commercial purposes.

Methods and Tools
Language & Frameworks: Python, Pandas, NumPy, Scikit-learn, TensorFlow/PyTorch
NLP: SpaCy, NLTK, Transformers (DistilBERT)
Visualization: Matplotlib, Seaborn, Plotly
APIs & Data Access: OpenFDA API, BeautifulSoup, Requests
Environment: Jupyter Notebook / Google Colab / Visual Studio Code

Project Structure
FDA_Project/
│
├── data/                # Raw and cleaned datasets
├── notebooks/           # Jupyter notebooks for EDA and modeling
├── scripts/             # Python scripts for scraping, cleaning, and training
├── outputs/             # Model outputs, plots, and reports
├── README.md            # Project overview (this file)
└── requirements.txt     # Dependencies

Current Progress
✅ Data scraping and extraction from FDA’s open datasets
✅ Text cleaning and preprocessing (tokenization, stop-word removal, lemmatization)
✅ Preliminary topic modeling and feature extraction
🔄 Ongoing: Model training and evaluation for regulation-study matching
🔄 Ongoing: Report writing and final presentation preparation

Team & Contributions
This project is being developed collaboratively by:
Peter Ogunrinde
Kay Michnicki
Dominique Fowler
as part of a class project at the University of San Diego.

Each team member is contributing to different aspects of the project, including:
FDA data collection - Kay
Data Exploration - Kay & Peter
Text preprocessing and data cleaning - Kay & Peter
Feature engineering and model development 
Analysis, documentation, and reporting

All contributions are collaborative and ongoing. A detailed summary of individual contributions and ownership will be finalized upon completion of the project to ensure proper credit and authorship acknowledgment.

License & Usage
This repository is for academic and educational use as part of a class project at the University of San Diego.
All contributors retain ownership of their individual work and original code developed during this project.
After the course concludes, contributors may continue developing their own versions, extensions, or derivative projects independently, provided they do not use another contributor’s specific code or proprietary content without permission.
The data used in this project are publicly available from FDA’s OpenFDA API and related sources.
