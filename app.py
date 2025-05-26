import streamlit as st
import pandas as pd
import openai

# --- Load Excel File ---
@st.cache_data
def load_data():
    return pd.read_excel("trlx_sh_pb_australia_commercial_msrp_aud_Q2_2025.xlsx", sheet_name=None)

excel_data = load_data()

# --- App Title ---
st.title("📊 Excel Q&A with OpenAI")

# --- OpenAI API Key Input ---
openai_api_key = st.text_input("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", type="password")

# --- User Question ---
question = st.text_input("❓ Ask a question about the spreadsheet")

if question and openai_api_key:
    all_text = ""

    # Search relevant data from all sheets
    for sheet_name, df in excel_data.items():
        df_str = df.astype(str)
        matching_rows = df_str[df_str.apply(lambda row: row.str.contains(question, case=False, na=False).any(), axis=1)]
        if not matching_rows.empty:
            all_text += f"\n\nFrom sheet: {sheet_name}\n"
            all_text += matching_rows.to_string(index=False)

    if not all_text.strip():
        all_text = "No matching rows were found in the spreadsheet, but please try answering based on general context."

    # --- Ask OpenAI using new SDK ---
    try:
        client = openai.OpenAI(api_key=openai_api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering questions based on spreadsheet content."},
                {"role": "user", "content": f"User's question: {question}\n\nHere is the spreadsheet data:\n{all_text}"}
            ],
            temperature=0.4,
            max_tokens=500
        )

        st.markdown("### 💬 Answer:")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error calling OpenAI: {e}")
