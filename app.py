import streamlit as st
import pandas as pd
from gemini_handler import generate_with_gemini

st.set_page_config(page_title="Genetik Varyant Yorumlama (Gemini)", layout="wide")
st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")

uploaded_file = st.file_uploader("CSV formatında genetik verinizi yükleyin", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Yüklenen Dosya:")
    st.dataframe(df.head())

    if st.button("🔎 Gemini ile Yorumla"):
        st.info("Yorumlar oluşturuluyor...")
        results = []

        for _, row in df.head(5).iterrows():
            prompt = f"""
You are a clinical geneticist. Use NCBI (https://www.ncbi.nlm.nih.gov/variation/view) as background knowledge.
Evaluate the following variant:

Chromosome: {row['CHROM']}
Position: {row['POS']}
Reference: {row['REF']}
Alternate: {row['ALT']}

Indicate:
- If it is pathogenic, likely pathogenic, benign or unknown
- Associated disease (if known)
- Summary from NCBI if available

Please summarize in English.
"""
            result = generate_with_gemini(prompt)
            results.append({
                "CHROM": row['CHROM'],
                "POS": row['POS'],
                "REF": row['REF'],
                "ALT": row['ALT'],
                "Gemini_Yorum": result
            })

        st.subheader("📄 Gemini Yorumları")
        st.dataframe(pd.DataFrame(results))