# Intelligent NLP System for Extracting and Structuring Key Information from FDA Regulatory.

AAI-590 Capstone Project - University of San Diego

This project is part of the AAI-590 Capstone in the Applied Artificial Intelligence Program at the University of San Diego (USD). It focuses on building machine learning and deep learning models to triage FDA adverse event reports and drug recalls using natural language processing.

### -- Project Status: Active / Near Completion (Module 7)

# RegInsightAI: FDA Adverse Events & Recalls Triage  
_AAI-590 Capstone Project - University of San Diego_


This repository contains our final capstone project code base. It implements an end-to-end machine learning pipeline that predicts:

- Whether a drug adverse event is **serious vs. non-serious**, and  
- The **recall class** (I / II / III) for drug product recalls  

using FDA-style narrative text and limited structured metadata, as a first step toward regulatory triage and, ultimately, regulation-matching.

> This README structure is adapted from the AAI program’s recommended README template. :contentReference[oaicite:0]{index=0}  

---

## Table of Contents

1. [Project Intro / Objective](#project-intro--objective)  
2. [Partner(s) / Contributor(s)](#partners--contributors)  
3. [Methods Used](#methods-used)  
4. [Technologies](#technologies)  
5. [Repository Structure](#repository-structure)  
6. [How to Install and Run](#how-to-install-and-run)  
7. [Mapping to Final Project Requirements](#mapping-to-final-project-requirements)  
8. [Project Description](#project-description)  
9. [License](#license)  
10. [Acknowledgments](#acknowledgments)  

---

## Project Intro / Objective

The main purpose of this project is to build a **regulatory triage assistant** for FDA-related text:

- For **adverse events**, the model predicts whether a case report is likely to be **serious**, so that safety teams can prioritize review.
- For **drug recalls**, the model predicts **recall class (I / II / III)** from the free-text reason for recall.

In practice, companies often receive unstructured narratives adverse reaction descriptions, internal quality deviations, and draft recall text before they have a clear mapping to FDA requirements. Our pipeline takes these narratives, learns patterns from historical data, and outputs risk-oriented predictions that can drive faster escalation and review.

Long term, this work is a stepping stone toward automatically **linking violations to specific FDA regulations and guidance documents**. For this capstone, we focus on classification tasks that are well supported by the available Kaggle/FDA data.

---

## Partner(s) / Contributor(s)

**Team Members**

- *Peter Ogunrinde* – Model training + optimization + evaluation, Deep learning (Keras), classical ML
- *Kay Michnicki* – Data cleaning, EDA, ML, Model optimization + evaluation 
- *Dominique Fowler* – Model Anaylsis, Documentation, report & presentation
This project is being developed collaboratively by:
Peter Ogunrinde, Kay Michnicki and Dominique Fowler as part of a class project at the University of San Diego.

Each team member is contributing to different aspects of the project, including:
- FDA data collection - Kay
- Data Exploration, gitHub - Kay & Peter
- Text preprocessing and data cleaning - Kay & Peter
- Model development. Model Training, Machine Learning Methods and Tools  - Kay & Peter
- Analysis, documentation, and reporting -  Kay, Peter, Dominique

---

## Methods Used

- Supervised Machine Learning  
  - Logistic Regression (TF–IDF features)  
  - Linear Support Vector Machines (LinearSVC)  
- Deep Learning (from scratch)  
  - Keras feed-forward network with text embeddings + tabular inputs  
- Natural Language Processing (NLP)  
  - Text cleaning and normalization  
  - TF–IDF vectorization  
  - Keras `TextVectorization` + `Embedding`  
- Model Evaluation & Optimization  
  - Train/validation/test splits  
  - GridSearchCV & cross-validation  
  - ROC/PR curves, confusion matrices, F1, macro-F1  
  - Validation curves, learning curves, threshold tuning  
- Model Analysis & Interpretability  
  - Top weighted features from linear models  
  - Age/sex risk plots  
  - Error analysis (misclassified examples)  

---

## Technologies

- **Language:** Python 3.x  
- **Core Libraries:**
  - `pandas`, `numpy`  
  - `scikit-learn` (Logistic Regression, LinearSVC, pipelines, metrics)  
  - `matplotlib`, `seaborn` (visualizations)  
  - `tensorflow` / `keras` (neural network from scratch)  
  - `json`, `datetime` (parsing nested and date fields)  

Jupyter Notebooks (`.ipynb`) are used as the main development and analysis environment.

---

## Repository Structure

A suggested final structure (what the instructor will see):

```text
aai590-reginsightai/
├─ README.md                          # This file
├─ requirements.txt                   # Python dependencies (optional but recommended)
├─ data/
│  ├─ raw/                            # (Optional; usually .gitignored if large)
│  └─ processed/                      # Cleaned / filtered CSVs (documented in notebook)
├─ notebooks/
│  ├─ finalCapstone_group2.ipynb      # Main end-to-end notebook
│  ├─ finalCapstone_group2.pdf        # PDF export of the notebook
│  └─ (optional) eda_only.ipynb       # Extra notebooks if used, with PDF exports
├─ src/
│  ├─ data_cleaning.py                # (Optional) helper functions for cleaning
│  ├─ models_classical.py             # (Optional) LR/SVM pipeline builders
│  ├─ models_nn.py                    # (Optional) Keras NN builder/training helpers
│  └─ analysis_utils.py               # (Optional) ROC/PR/confusion matrix utilities
└─ reports/
   └─ AAI590_Final_Report.pdf         # Final written report (Part 1)
```

Project Overview

This project explores how publicly available FDA data can be used to analyze, model, and understand regulatory activities related to drugs, biologics, and medical devices.
The primary goal is to clean, structure, and model FDA datasets to identify relationships between regulations, recalls, and adverse events and to explore whether machine learning techniques can predict which regulations may apply to a given product or study type.
This work aims to build a foundation for an intelligent search and recommendation system that links study requirements or product features to relevant FDA regulations and guidance documents.

#### Datasets

We use open FDA datasets from the OpenFDA API, including:
Regulatory and Guidance Documents (Drugs, Devices, Biologics)
Recalls and Enforcement Reports
Adverse Events Data
All data are publicly available and used strictly for academic and non-commercial purposes.
---

## How to Install and Run
**1. Clone the Repository**
```
git clone https://github.com/pogunrinde/AAI-590-FinalCapstone.git
cd AAI-590-FinalCapstone

```
---

## How to Install and Run
**2. Create and Activate an Environment**
``` Using pip:

python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```
Or using `conda` (if you choose to provide `environment.yml`):

```
conda env create -f environment.yml
conda activate AAI-590-FinalCapstone

```

**3. Data Setup**

Place raw FDA / Kaggle data in data/raw/ (or update paths at the top of the notebook).

The notebook will write cleaned/intermediate outputs to data/processed/ as needed.

**4. Run the Main Notebook**

Open Jupyter Lab/Notebook:

```
jupyter lab
# or
jupyter notebook

```

Then open:

```
notebooks/AAI-590-FinalCapstone.ipynb
```


Run all cells from top to bottom to reproduce:
1. Data Cleaning
2. Exploratory Data Analysis (EDA)
3. Model Design/Building (classical + NN)
4. Model Training
5. Model Optimization (validation/learning curves, threshold tuning)
6. Model Analysis (ROC/PR, confusion matrices, feature weights, age/sex plots, error analysis)

To support grading, also export the notebook to PDF (already included as finalCapstone_group2.pdf).

---

**Current Progress**

✅ Data scraping and extraction from FDA’s open datasets

✅ Text cleaning and preprocessing (tokenization, stop-word removal, lemmatization)

✅ Preliminary topic modeling and feature extraction

✅ Model training and evaluation for regulation-study matching

🔄 Ongoing: Report writing and final presentation preparation



**License & Usage**

This repository is for academic and educational use as part of a class project at the University of San Diego.
All contributors retain ownership of their individual work and original code developed during this project.
After the course concludes, contributors may continue developing their own versions, extensions, or derivative projects independently, provided they do not use another contributor’s specific code or proprietary content without permission.
The data used in this project are publicly available from FDA’s OpenFDA API and related sources.



**Acknowledgments**

We would like to thank:
- Course instructor and teaching staff for guidance on project scope, feedback on drafts, and clarification of requirements.
- The MS-AAI program at the University of San Diego for providing the capstone structure and README template guidance.
- The maintainers of scikit-learn, TensorFlow/Keras, and other open-source libraries used in this project.
- Data providers at FDA and Kaggle for making regulatory and safety-related datasets publicly accessible.
