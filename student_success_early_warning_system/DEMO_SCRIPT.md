# 5–6 Minute Presentation and Demo Script

## 0:00–0:30 — Introduction
Hello, I’m Khizar Nawaz. My Applied AI internship project is an AI-Based Student Performance Prediction System. It estimates a final Mathematics grade and provides a transparent academic-support indicator.

## 0:30–1:10 — Problem
Student performance is shaped by academic history, family context, support, attendance, and social factors. Looking at one factor at a time can miss patterns. This project demonstrates how machine learning can combine historical signals to support earlier academic conversations.

## 1:10–1:50 — Solution
The system takes structured student information, preprocesses it safely, compares several regression models, selects the strongest model, and exposes it through a simple Streamlit interface. The output is a predicted grade out of 20, a project-defined performance category, and a non-clinical support indicator.

## 1:50–2:40 — Dataset and workflow
I used the official UCI Student Performance dataset and chose the Mathematics subset, which has 395 records. The target is G3, the final grade. The workflow includes validation, encoding categorical values, scaling numeric values, an 80/20 holdout split, training, evaluation, model saving, and deployment.

An important design decision is G1 and G2: they are previous-period grades. They are useful when those grades are already available. I also trained an early-stage comparison without them, which is more difficult and is reported separately.

## 2:40–3:30 — Models and evaluation
I compared Linear Regression, Random Forest, Gradient Boosting, and Extra Trees using MAE, RMSE, and R-squared. On this trained run, the project selected the lowest-RMSE model. I will use the metrics shown on this slide, which come directly from the saved report.

## 3:30–5:15 — Live demo
Now I’ll open the Streamlit application. The inputs are grouped into student information, academic information, family/support information, and lifestyle/wellbeing. I’ll enter a realistic example, including G1 and G2, and click Predict Performance.

The application returns a final-grade estimate out of 20, a clearly defined performance category, and an academic-support indicator. These are discussion prompts, not diagnoses or final decisions. Below the result, the app shows the most influential transformed features from the selected model and an expandable summary of the entered information.

## 5:15–5:45 — Conclusion
To conclude, this project demonstrates a complete Applied AI workflow: trustworthy source data, reusable preprocessing, comparison of multiple models, actual evaluation, explainability, testing, and a usable interface. A future version would use more representative data and fairness and uncertainty analysis. Thank you.
