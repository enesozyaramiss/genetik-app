import streamlit as st
import pandas as pd
from gemini_handler import generate_with_gemini
from clinvar_api import get_clinvar_data

# Sayfa ayarları
st.set_page_config(page_title="Genetik Varyant Yorumlama (Gemini)", layout="wide")
st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")

# CSV dosyası yükleyici
uploaded_file = st.file_uploader("CSV formatında genetik verinizi yükleyin", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📄 Yüklenen Dosya:")
    st.dataframe(df.head())

    if st.button("🔎 Gemini ile Yorumla"):
        st.info("Yorumlar oluşturuluyor... Lütfen bekleyin.")
        results = []

        # İlk 5 varyant için dön
        for _, row in df.head(5).iterrows():
            chrom = row["CHROM"]
            pos = row["POS"]
            ref = row["REF"]
            alt = row["ALT"]
            rsid = str(row.get("Sample_ID", "")).replace("rs", "")  # Sample_ID'den rsID çekiyoruz

            # ClinVar’dan bilgi al
            clinvar_summary = get_clinvar_data(rsid) if rsid else "No ClinVar ID available."

            # Gemini’ye gönderilecek prompt
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

            # Gemini ile yanıt al
            result = generate_with_gemini(prompt)

            # Sonuçları listeye ekle
            results.append({
                "Sample_ID": f"rs{rsid}" if rsid else "N/A",
                "CHROM": chrom,
                "POS": pos,
                "REF": ref,
                "ALT": alt,
                "Gemini_Yorum": result
            })

        # Sonuçları göster
        st.subheader("📊 Gemini Yorumları")
        st.dataframe(pd.DataFrame(results))
