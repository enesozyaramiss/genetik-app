import streamlit as st
import pandas as pd
import gzip, io, time

from clinvar_parser import enrich_clinvar_df, add_gnomad_links, fetch_gnomad_simple
from gemini_handler import generate_with_gemini
from clingen_handler import load_clingen_validity, get_clingen_classification
from pubmed_handler import get_pubmed_ids_from_clinvar, build_pubmed_links

# ClinVar + ClinGen setup
clinvar_df = enrich_clinvar_df(pd.read_parquet("sampled_100.parquet"))
clinvar_df = add_gnomad_links(clinvar_df, genome_build="GRCh38")
clingen_df = load_clingen_validity("Clingen-Gene-Disease-Summary-2025-07-01.csv")

# VCF parser’lar (aynı)
def parse_vcf_gz(uploaded_file, start=0, end=300):
    rows=[]; idx=0
    with gzip.open(io.BytesIO(uploaded_file.read()), 'rt') as f:
        for line in f:
            if line.startswith("#"): continue
            if start <= idx < end:
                p=line.split("\t")
                rows.append({"CHROM": p[0], "POS": int(p[1]), "REF":p[3], "ALT":p[4]})
            idx+=1
            if idx>=end: break
    return pd.DataFrame(rows)

def parse_vcf(uploaded_file, start=0, end=300):
    lines = uploaded_file.getvalue().decode().splitlines()
    rows=[]; idx=0
    for line in lines:
        if line.startswith("#"): continue
        if start <= idx < end:
            p=line.split("\t")
            rows.append({"CHROM": p[0], "POS": int(p[1]), "REF":p[3], "ALT":p[4]})
        idx+=1
        if idx>=end: break
    return pd.DataFrame(rows)

# Streamlit UI
st.set_page_config(page_title="Genetik Varyant Yorumlama", layout="wide")
st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")
uploaded = st.file_uploader("📁 Dosya yükle (.vcf/.vcf.gz/.csv)", type=["vcf","vcf.gz","csv"])

if uploaded:
    if uploaded.name.endswith(".vcf.gz"):
        df = parse_vcf_gz(uploaded)
    elif uploaded.name.endswith(".vcf"):
        df = parse_vcf(uploaded)
    else:
        df = pd.read_csv(uploaded)

    if st.button("🔎 Gemini ile Yorumla"):
        with st.spinner("🧠 Gemini yorumluyor..."):
            # Tip dönüşümleri ve merge
            for c in ["CHROM","POS","REF","ALT"]:
                df[c]=df[c].astype(str); clinvar_df[c]=clinvar_df[c].astype(str)
            merged = pd.merge(df, clinvar_df, on=["CHROM","POS","REF","ALT"], how="left")
            merged["ClinGen_Validity"] = merged["GENE"].apply(lambda g: get_clingen_classification(g, clingen_df))
            matched = merged[~merged["ID"].isna()].copy()

            st.write(f"✅ Eşleşen varyant sayısı: {len(matched)}")
            st.dataframe(matched.head(30))

            results=[]
            for i, row in matched.iterrows():
                st.write(f"🔍 {i+1}. {row['CHROM']}:{row['POS']} {row['REF']}>{row['ALT']}")

                # PubMed
                ids = []
                if not pd.isna(row["ID"]):
                    try:
                        ids = get_pubmed_ids_from_clinvar(str(int(row["ID"])))
                    except: pass
                links = build_pubmed_links(ids)

                # gnomAD API
                stats = fetch_gnomad_simple(row["CHROM"], row["POS"], row["REF"], row["ALT"])
                # Uyarı al
                if not stats:
                    st.warning(f"⚠️ gnomAD yok: {row['CHROM']}-{row['POS']}-{row['REF']}-{row['ALT']}")

                # Prompt
                prompt = f"""
You are a clinical geneticist. Based on the following variant and annotation data, provide a professional clinical interpretation.

🧬 Variant:
- Chr: {row['CHROM']}, Pos: {row['POS']}, {row['REF']}→{row['ALT']}

📑 ClinVar:
- Gene: {row.get('GENE','N/A')}, Sig: {row.get('CLNSIG','N/A')}, Dis: {row.get('DISEASE','N/A')}

🧪 ClinGen Validity: {row.get('ClinGen_Validity','N/A')}

📚 PubMed: {', '.join(links) if links else 'None'}

📊 gnomAD:
- Link: {row.get('gnomAD_Link','N/A')}
- Exome AC/AN: {stats.get('Exome_AC','N/A')}/{stats.get('Exome_AN','N/A')}
- PopMax AF: {stats.get('PopMax_AF','N/A')} (Pop: {stats.get('PopMax_Pop','N/A')})

🩺 Answer:
1. Likely pathogenicity?
2. Known disease?
3. Clinical relevance?
4. Plain-language summary (≤5 sents).
"""
                try:
                    yorum = generate_with_gemini(prompt)
                except Exception as e:
                    yorum = f"❌ {e}"

                results.append({
                    **row.to_dict(),
                    "PubMed_Links": links,
                    **stats,
                    "Gemini_Yorum": yorum
                })
                time.sleep(0.3)

        st.success("✅ Tamamlandı")
        st.subheader("📊 Sonuçlar")
        st.dataframe(pd.DataFrame(results))
