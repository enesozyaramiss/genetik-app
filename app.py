import streamlit as st
import pandas as pd
import requests
import time
from gemini_handler import generate_with_gemini  # Bu fonksiyon senin kendi Gemini API 
import gzip


def parse_vcf_gz(file, start=100, end=110):
    rows = []
    count = 0

    with gzip.open(file, 'rt') as f:  # 'rt' = read text
        for line in f:
            if line.startswith("#"):
                continue
            if count >= start and count < end:
                parts = line.strip().split("\t")
                if len(parts) >= 5:
                    chrom = parts[0]
                    pos = parts[1]
                    ref = parts[3]
                    alt = parts[4]
                    rows.append({
                        "CHROM": chrom,
                        "POS": pos,
                        "REF": ref,
                        "ALT": alt
                    })
            count += 1
            if count >= end:
                break

    return pd.DataFrame(rows)

# 🧬 HGVS formatı oluştur
def create_hgvs(chrom, pos, ref, alt):
    return f"{chrom}:g.{pos}{ref}>{alt}"

# 🔍 Variation ID al
def get_variation_id(hgvs_str):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "clinvar", "term": hgvs_str, "retmode": "json"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [None])[0]
    except:
        return None

# 🔬 ClinVar detaylarını getir
def get_clinvar_info(variation_id):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {"db": "clinvar", "id": variation_id, "retmode": "json"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        uid = data["result"]["uids"][0]
        result = data["result"][uid]

        traits = [t.get("trait_name") for t in result.get("germline_classification", {}).get("trait_set", [])]
        return {
            "title": result.get("title", "Yok"),
            "gene": result.get("genes", [{}])[0].get("symbol", "Yok"),
            "clinical_significance": result.get("germline_classification", {}).get("description", "Yok"),
            "condition": ", ".join(traits) if traits else "Yok",
            "review_status": result.get("germline_classification", {}).get("review_status", "Yok")
        }
    except:
        return {
            "title": "Yok",
            "gene": "Yok",
            "clinical_significance": "Yok",
            "condition": "Yok",
            "review_status": "Yok"
        }

# 🌐 Streamlit arayüzü
st.set_page_config(page_title="Genetik Varyant Yorumlama (Gemini)", layout="wide")
st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")

uploaded_file = st.file_uploader("Genetik veri dosyanızı yükleyin (.vcf, .vcf.gz veya .csv)", type=["vcf", "vcf.gz", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".vcf.gz"):
        df = parse_vcf_gz(uploaded_file)
    elif uploaded_file.name.endswith(".vcf"):
        df = parse_vcf(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    st.write("📄 İlk 100 Varyant:")
    st.dataframe(df.head())

    if st.button("🔎 Gemini ile Yorumla"):
        st.info("Yorumlar oluşturuluyor... Lütfen bekleyin.")
        results = []

        for i, row in df.iterrows():
            chrom = row["CHROM"]
            pos = row["POS"]
            ref = row["REF"]
            alt = row["ALT"]

            hgvs = create_hgvs(chrom, pos, ref, alt)
            variation_id = get_variation_id(hgvs)
            clinvar = get_clinvar_info(variation_id) if variation_id else {}

            # 🧠 Gemini prompt
            prompt = f"""
You are a clinical geneticist.

Variant Info:
- Chromosome: {chrom}
- Position: {pos}
- Reference: {ref}
- Alternate: {alt}

ClinVar Info:
- Title: {clinvar.get("title", "Yok")}
- Gene: {clinvar.get("gene", "Yok")}
- Clinical Significance: {clinvar.get("clinical_significance", "Yok")}
- Condition: {clinvar.get("condition", "Yok")}
- Review Status: {clinvar.get("review_status", "Yok")}

Interpret this variant and provide:
- Likely pathogenicity
- Associated disease (if any)
- Clinical relevance
- A concise medical summary in plain language
"""

            gemini_response = generate_with_gemini(prompt)

            results.append({
                "CHROM": chrom,
                "POS": pos,
                "REF": ref,
                "ALT": alt,
                "Gene": clinvar.get("gene", "Yok"),
                "Condition": clinvar.get("condition", "Yok"),
                "Significance": clinvar.get("clinical_significance", "Yok"),
                "Gemini_Yorum": gemini_response
            })

            time.sleep(0.34)  # NCBI rate-limit güvenliği

        # 📊 Sonuçları göster
        st.subheader("📊 Yorumlanan Varyantlar")
        st.dataframe(pd.DataFrame(results))
