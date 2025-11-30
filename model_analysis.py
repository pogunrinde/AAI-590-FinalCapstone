"""
RegInsightAI - Model Analysis Module
AAI-590 Capstone Project
Author: Dominique Fowler
Description: Utilities for visualizing model performance and feature importance
             for FDA Regulatory text classification.

Deployment Instructions:
    1. Upload this file to the same directory as your notebook.
    2. Import the module:
       import model_analysis as ma
    
    3. Generate visualizations:
       # Confusion Matrix
       ma.plot_confusion_matrix(y_test, y_pred, labels=['Non-Serious', 'Serious'])
       
       # Feature Importance (Linear Models only)
       ma.plot_feature_importance(model, tfidf_vectorizer, top_n=15)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

# Set style for consistency across the report
plt.style.use('ggplot')

def plot_confusion_matrix(y_true, y_pred, labels=['Non-Serious', 'Serious'], title='Confusion Matrix'):
    """
    Generates a heatmap for binary classification.
    Focus is on identifying False Negatives (Serious events classified as Non-Serious).
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    # Using 'Blues' to match our presentation theme
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=labels, yticklabels=labels)
    
    plt.title(title)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    
    # Save with high DPI for the final report
    plt.savefig('confusion_matrix_fda.png', dpi=300)
    print(">> Saved confusion_matrix_fda.png")
    plt.show()

def plot_feature_importance(model, vectorizer, top_n=15):
    """
    Extracts coefficients from Linear models (LogReg/SVM) to determine
    which words drive the 'Serious' vs 'Non-Serious' classification.
    """
    # Safety check for linear models
    if not hasattr(model, 'coef_'):
        print("Warning: Model is not linear (no coefficients found). Skipping feature plot.")
        return

    print("Extracting feature importance...")
    feature_names = vectorizer.get_feature_names_out()
    coefs = model.coef_.flatten()
    
    df_feat = pd.DataFrame({'word': feature_names, 'importance': coefs})
    df_feat = df_feat.sort_values('importance', ascending=False)
    
    # Grab the strongest predictors for both classes
    top_features = pd.concat([df_feat.head(top_n), df_feat.tail(top_n)])
    
    plt.figure(figsize=(10, 8))
    # Color code: Red for Non-Serious (Negative), Blue for Serious (Positive)
    colors = ['#1f77b4' if x > 0 else '#d62728' for x in top_features['importance']]
    
    plt.barh(top_features['word'], top_features['importance'], color=colors)
    plt.title(f'Top {top_n} Terms Predicting Severity (FDA Dataset)')
    plt.xlabel('Coefficient Magnitude')
    plt.axvline(0, color='black', linewidth=0.8) # Center line
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    plt.savefig('feature_importance_fda.png', dpi=300)
    print(">> Saved feature_importance_fda.png")
    plt.show()

if __name__ == "__main__":
    # Test block: Runs if script is executed directly
    print("Running test generation...")
    
    # Generate dummy data to verify plots work
    y_test = [0, 1, 0, 1, 1, 0, 0, 1]
    y_pred = [0, 1, 0, 0, 1, 0, 1, 1]
    plot_confusion_matrix(y_test, y_pred)
    print("Test complete.")