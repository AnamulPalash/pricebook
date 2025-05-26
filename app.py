import streamlit as st
import pandas as pd

st.title("Pricebook Search Australia - Q2 2025")

# Load Excel file
@st.cache_data
def load_data():
    return pd.read_excel("pricebook_au_q2-2025.xlsx", sheet_name=None)

excel_data = load_data()

# Input search query
query = st.text_input("🔍 Enter a keyword to search:")

if query:
    for sheet_name, df in excel_data.items():
        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]
        if not results.empty:
            st.subheader(f"Results from sheet: {sheet_name}")
            st.dataframe(results)
