import streamlit as st
import pandas as pd
import gzip
import io
import time

from clinvar_parser import enrich_clinvar_df
from gemini_handler import generate_with_gemini
from clingen_handler import load_clingen_validity, get_clingen_classification
from pubmed_handler import get_pubmed_ids_from_clinvar, build_pubmed_links

# 📦 ClinVar verisi (önceden hazırlanmış Parquet formatında)
clinvar_df = pd.read_parquet("sampled_100.parquet")
clinvar_df = enrich_clinvar_df(clinvar_df)


# 🧬 ClinGen verisini yükle
clingen_df = load_clingen_validity("Clingen-Gene-Disease-Summary-2025-07-01.csv")


# 📥 VCF.GZ Dosyasını Oku
def parse_vcf_gz(uploaded_file, start=0, end=2000):
    rows = []
    data_row_index = 0
    with gzip.open(io.BytesIO(uploaded_file.read()), 'rt') as f:
        for line in f:
            if line.startswith("#"):
                continue
            if start <= data_row_index < end:
                parts = line.strip().split("\t")
                if len(parts) >= 5:
                    rows.append({
                        "CHROM": parts[0],
                        "POS": int(parts[1]),
                        "REF": parts[3],
                        "ALT": parts[4]
                    })
            data_row_index += 1
            if data_row_index >= end:
                break
    return pd.DataFrame(rows)

# 📥 Düz VCF Dosyasını Oku
def parse_vcf(uploaded_file, start=0, end=2000):
    rows = []
    data_row_index = 0
    for line in uploaded_file.getvalue().decode("utf-8").splitlines():
        if line.startswith("#"):
            continue
        if start <= data_row_index < end:
            parts = line.strip().split("\t")
            if len(parts) >= 5:
                rows.append({
                    "CHROM": parts[0],
                    "POS": int(parts[1]),
                    "REF": parts[3],
                    "ALT": parts[4]
                })
        data_row_index += 1
        if data_row_index >= end:
            break
    return pd.DataFrame(rows)

# 🌐 Uygulama Arayüzü
st.set_page_config(page_title="Genetik Varyant Yorumlama", layout="wide")
st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")

uploaded_file = st.file_uploader("📁 Dosya yükle (.vcf, .vcf.gz, .csv)", type=["vcf", "vcf.gz", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".vcf.gz"):
        df = parse_vcf_gz(uploaded_file)
    elif uploaded_file.name.endswith(".vcf"):
        df = parse_vcf(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    if st.button("🔎 Gemini ile Yorumla"):
        with st.spinner("🧠 Gemini yorumluyor... Lütfen bekleyin."):
            results = []


            # Tüm merge edilecek sütunları aynı tipe dönüştür
            for col in ["CHROM", "POS", "REF", "ALT"]:
                df[col] = df[col].astype(str)
                clinvar_df[col] = clinvar_df[col].astype(str)
            merged_df = pd.merge(df, clinvar_df, on=["CHROM", "POS", "REF", "ALT"], how="left")
            merged_df["ClinGen_Validity"] = merged_df["GENE"].apply(lambda g: get_clingen_classification(g, clingen_df))

            matched_df = merged_df[~merged_df["ID"].isna()].copy()
            st.write(f"✅ Eşleşen varyant sayısı: {len(matched_df)}")
            st.dataframe(matched_df.head(50))

            for i, row in matched_df.iterrows():
                st.write(f"🔍 {i+1}. varyant işleniyor: {row['CHROM']}:{row['POS']} {row['REF']}>{row['ALT']}")

                variation_id = row.get("ID")
                if pd.isna(variation_id):
                    pubmed_ids = []
                    st.write("ℹ️ ID boş, PubMed eşlemesi yapılmadı.")
                else:
                    try:
                        variation_id = str(int(variation_id))  # float -> int -> str
                        pubmed_ids = get_pubmed_ids_from_clinvar(variation_id)
                    except Exception as e:
                        pubmed_ids = []
                        st.write(f"⚠️ PubMed ID sorgusunda hata: {e}")

                pubmed_links = build_pubmed_links(pubmed_ids)

                
                prompt = f"""
You are a clinical geneticist.

Variant Info:
- Chromosome: {row['CHROM']}
- Position: {row['POS']}
- Reference: {row['REF']}
- Alternate: {row['ALT']}

ClinVar Info:
- Gene: {row.get('GENE', 'Yok')}
- Clinical Significance: {row.get('CLNSIG', 'Yok')}
- Disease: {row.get('DISEASE', 'Yok')}

ClinGen Info:
- Gene-Disease Validity Classification: {row.get('ClinGen_Validity', 'Yok')}

PubMed Articles:
- {', '.join(pubmed_links) if pubmed_links else 'Yok'}

Interpret this variant and provide:
- Likely pathogenicity
- Associated disease (if any)
- Clinical relevance
- A concise medical summary in plain language
"""
                try:
                    yorum = generate_with_gemini(prompt)
                except Exception as e:
                    yorum = f"❌ Hata: {str(e)}"

                results.append({**row, "PubMed_Links": pubmed_links, "Gemini_Yorum": yorum})
                time.sleep(0.4)

        st.success("✅ Yorumlama tamamlandı!")
        st.subheader("📊 Yorumlanan Varyantlar")
        st.dataframe(pd.DataFrame(results))
