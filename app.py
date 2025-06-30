import streamlit as st
import pandas as pd
from gemini_handler import generate_with_gemini
from clinvar_api import get_clinvar_data

def parse_vcf(file):
    lines = file.readlines()
    rows = []
    for line in lines:
        decoded = line.decode("utf-8")
        if decoded.startswith("#"):
            continue  # başlık satırlarını atla
        parts = decoded.strip().split("\t")
        if len(parts) >= 5:
            chrom = parts[0]
            pos = parts[1]
            id_field = parts[2]
            ref = parts[3]
            alt = parts[4]
            rows.append({
                "CHROM": chrom,
                "POS": pos,
                "Sample_ID": id_field,  # rsID olabilir
                "REF": ref,
                "ALT": alt
            })
    return pd.DataFrame(rows)

# Sayfa ayarları
st.set_page_config(page_title="Genetik Varyant Yorumlama (Gemini)", layout="wide")
st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")

uploaded_file = st.file_uploader("Genetik veri dosyanızı yükleyin (.csv veya .vcf)", type=["csv", "vcf"])

if uploaded_file:
    if uploaded_file.name.endswith(".vcf"):
        df = parse_vcf(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    st.write("📄 Yüklenen Veri:")
    st.dataframe(df.head())

    if st.button("🔎 Gemini ile Yorumla"):
        st.info("Yorumlar oluşturuluyor... Lütfen bekleyin.")
        results = []

        for _, row in df.head(5).iterrows():
            chrom = row["CHROM"]
            pos = row["POS"]
            ref = row["REF"]
            alt = row["ALT"]
            rsid = str(row.get("Sample_ID", "")).replace("rs", "")

            # ClinVar verisi
            clinvar_summary = get_clinvar_data(rsid) if rsid else "No ClinVar ID available."

            prompt = f"""
You are a clinical geneticist.

Variant Info:
Chromosome: {chrom}
Position: {pos}
Reference: {ref}
Alternate: {alt}

ClinVar Info (for rsID: rs{rsid}):
{clinvar_summary}

Interpret this variant and provide:
- Likely pathogenicity
- Associated disease (if any)
- Clinical relevance
- Summary
"""
            result = generate_with_gemini(prompt)

            results.append({
                "Sample_ID": f"rs{rsid}" if rsid else "N/A",
                "CHROM": chrom,
                "POS": pos,
                "REF": ref,
                "ALT": alt,
                "Gemini_Yorum": result
            })

        st.subheader("📊 Gemini Yorumları")
        st.dataframe(pd.DataFrame(results))
