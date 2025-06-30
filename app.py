import streamlit as st
import pandas as pd
from biogpt_handler import generate_explanation

st.set_page_config(page_title="Genetik Varyant Yorumlama", layout="wide")
st.title("🧬 BioGPT Destekli Genetik Varyant Yorumlama Uygulaması")

uploaded_file = st.file_uploader(".csv formatındaki VCF dosyanızı yükleyin", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Yüklenen Dosya:")
    st.dataframe(df.head())

    if st.button("🧠 Yorumları Oluştur"):
        st.write("Yorumlar oluşturuluyor, lütfen bekleyin...")
        prompts = []
        results = []

        for _, row in df.head(5).iterrows():
            prompt = f"""You are a clinical geneticist. Please interpret the following genetic variant:
Chromosome: {row['CHROM']}
Position: {row['POS']}
Reference: {row['REF']}
Alternate: {row['ALT']}
INFO: {row.get('INFO', 'N/A')}

Provide:
- Likely pathogenicity
- Associated disease (if known)
- Clinical relevance
- Any known references (ClinVar / dbSNP)
"""
            response = generate_explanation(prompt)
            results.append({
                "CHROM": row['CHROM'],
                "POS": row['POS'],
                "REF": row['REF'],
                "ALT": row['ALT'],
                "BioGPT_Yorum": response
            })

        st.subheader("📄 BioGPT Yorumları")
        st.dataframe(pd.DataFrame(results))