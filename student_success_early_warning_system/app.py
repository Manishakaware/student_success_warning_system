import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from data_preprocessing import load_dataset
from predict import academic_support_indicator, load_model, performance_category, predict_grade

st.set_page_config(page_title="AI Student Performance Predictor", page_icon="🎓", layout="wide")
st.markdown("""<style>.block-container{max-width:1200px;padding-top:2rem}.stMetric{background:#f8fafc;border-radius:12px;padding:16px}</style>""", unsafe_allow_html=True)
@st.cache_resource
def get_model(): return load_model()
@st.cache_data
def get_data(): return load_dataset()

data = get_data(); model = get_model()
with open(ROOT / "reports" / "training_metadata.json", encoding="utf-8") as source: metadata = json.load(source)
st.sidebar.title("Project information")
st.sidebar.write("**Dataset:** UCI Student Performance (Mathematics)")
st.sidebar.write(f"**Model:** {metadata['best_model']}")
st.sidebar.caption("Official source: archive.ics.uci.edu/dataset/320/student+performance")
st.sidebar.divider(); st.sidebar.caption("Educational ML prototype only. Predictions support discussion; they are not definitive judgments about a student's ability or future.")
st.title("🎓 AI Student Performance Predictor")
st.write("Estimate a student’s final Mathematics grade (G3) from academic, demographic, social, and behavioural information.")
st.info("The project-defined performance and support labels are transparent academic-support indicators, not clinical or psychological diagnoses.")

labels = {"famsize":"Family size", "Pstatus":"Parental cohabitation", "Medu":"Mother’s education", "Fedu":"Father’s education", "Mjob":"Mother’s job", "Fjob":"Father’s job", "traveltime":"Travel time", "studytime":"Weekly study time", "failures":"Previous failures", "schoolsup":"School support", "famsup":"Family support", "paid":"Paid classes", "famrel":"Family relationship quality", "freetime":"Free time", "goout":"Going out", "Dalc":"Workday alcohol consumption", "Walc":"Weekend alcohol consumption", "G1":"First-period grade (G1)", "G2":"Second-period grade (G2)", "G3":"Final grade"}
groups = {"Student Information":["school","sex","age","address","famsize","Pstatus","guardian"], "Academic Information":["studytime","failures","absences","G1","G2","traveltime","reason"], "Family / Support Information":["Medu","Fedu","Mjob","Fjob","schoolsup","famsup","paid","higher","internet","nursery"], "Lifestyle / Wellbeing":["activities","romantic","famrel","freetime","goout","Dalc","Walc","health"]}
def display_name(column): return labels.get(column, column.replace("_", " ").title())
def input_for(column):
    values = data[column]
    if pd.api.types.is_numeric_dtype(values):
        low, high, default = int(values.min()), int(values.max()), int(values.median())
        return st.number_input(display_name(column), min_value=low, max_value=high, value=default, step=1)
    options = sorted(values.dropna().unique().tolist())
    if set(options).issubset({"yes","no"}):
        selected = st.radio(display_name(column), options, horizontal=True)
    else: selected = st.selectbox(display_name(column), options)
    return selected
inputs = {}
for heading, columns in groups.items():
    st.subheader(heading)
    columns_ui = st.columns(3)
    for index, column in enumerate(columns):
        with columns_ui[index % 3]: inputs[column] = input_for(column)
if st.button("Predict Performance", type="primary", use_container_width=True):
    grade = predict_grade(model, inputs); category = performance_category(grade); support = academic_support_indicator(grade)
    st.divider(); st.subheader("Prediction")
    first, second, third = st.columns(3); first.metric("Predicted Final Grade", f"{grade:.1f} / 20"); second.metric("Performance Category", category); third.metric("Academic-Support Indicator", support)
    st.caption("Performance categories: 16–20 Excellent; 14–<16 Very Good; 12–<14 Good; 10–<12 Average; <10 At Risk.")
    st.subheader("What factors matter most?")
    importance = pd.DataFrame(metadata["top_features"]).head(10).sort_values("Importance")
    figure, axis = plt.subplots(figsize=(8,4)); axis.barh(importance.Feature, importance.Importance, color="#14b8a6"); axis.set_xlabel("Model importance"); st.pyplot(figure, clear_figure=True)
    with st.expander("Entered student information"): st.dataframe(pd.DataFrame([inputs]), use_container_width=True, hide_index=True)
