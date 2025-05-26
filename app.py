import streamlit as st
import pandas as pd
import openai

# --- Load Excel File ---
@st.cache_data
def load_data():
    return pd.read_excel("pricebook_au_q2-2025.xlsx", sheet_name=None)

excel_data = load_data()

# --- App Title ---
st.title("ANZ Pricebook - Q2 2025")

# --- OpenAI API Key Input (or set it manually below) ---
openai_api_key = st.secrets["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"] if "openai_api_key" in st.secrets else st.text_input("🔑 Enter your OpenAI API key", type="password")

# --- User Question ---
question = st.text_input("What information you need from our pricebook?")

if question and openai_api_key:
    all_text = ""

    # Collect context from all sheets
    for sheet_name, df in excel_data.items():
        df_str = df.astype(str)
        matching_rows = df_str[df_str.apply(lambda row: row.str.contains(question, case=False, na=False).any(), axis=1)]
        if not matching_rows.empty:
            all_text += f"\n\nFrom sheet: {sheet_name}\n"
            all_text += matching_rows.to_string(index=False)

    if not all_text.strip():
        all_text = "No directly matching data found. But answer generally."

    # --- Ask OpenAI ---
    try:
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You're a helpful assistant answering questions based on the pricebook content."},
                {"role": "user", "content": f"User question: {question}\n\nPriceook content:\n{all_text}"}
            ],
            temperature=0.4,
            max_tokens=500
        )
        st.markdown("### 💬 Answer:")
        st.write(response['choices'][0]['message']['content'])
    except Exception as e:
        st.error(f"Error calling OpenAI: {e}")
