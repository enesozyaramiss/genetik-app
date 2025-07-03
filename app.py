import os
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import gzip, io, time
from functools import lru_cache
from clinvar_parser import enrich_clinvar_df, add_gnomad_links, fetch_gnomad_simple
from gemini_handler import generate_with_gemini
from clingen_handler import load_clingen_validity, get_clingen_classification
from pubmed_handler import get_pubmed_ids_from_clinvar, build_pubmed_links

# Sayfa yapılandırması
st.set_page_config(page_title="Genetik App", layout="wide")

# — Sidebar’daki şık menü —
with st.sidebar:
    selected = option_menu(
        menu_title="📑 Menü",
        options=["Uygulama", "Dokümantasyon"],
        icons=["house", "file-earmark-text"],   # Bootstrap ikon isimleri
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0px 0px 20px 0px"},
            "icon": {"font-size": "18px"}, 
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "--hover-color": "#f0f0f0"
            },
            "nav-link-selected": {
                "background-color": "#d9534f",
                "color": "white",
            },
        }
    )

if selected == "Dokümantasyon":
    from docs import show_documentation
    show_documentation()   # burada dokümantasyon modülündeki fonksiyonu çalıştırır


# Cache’lenmiş fonksiyonlar
# TTL: 24 saat (saniye cinsinden)
@st.cache_data(ttl=24 * 3600, show_spinner=False)
def get_pubmed_ids_cached(variation_id: str):
    return get_pubmed_ids_from_clinvar(variation_id)

@st.cache_data(ttl=24 * 3600, show_spinner=False)
def fetch_gnomad_cached(chrom: str, pos: str, ref: str, alt: str):
    return fetch_gnomad_simple(chrom, pos, ref, alt)
# -----------------------------


# ClinVar + ClinGen setup
clinvar_df = enrich_clinvar_df(pd.read_parquet("sampled_100.parquet"))
clinvar_df = add_gnomad_links(clinvar_df, genome_build="GRCh38")
clingen_df = load_clingen_validity("Clingen-Gene-Disease-Summary-2025-07-01.csv")

def parse_vcf_gz(uploaded_file):
    """Tüm veri satırlarını okur."""
    rows = []
    with gzip.open(io.BytesIO(uploaded_file.read()), 'rt') as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.strip().split("\t")
            rows.append({
                "CHROM": p[0],
                "POS": int(p[1]),
                "REF": p[3],
                "ALT": p[4]
            })
    return pd.DataFrame(rows)


def parse_vcf(uploaded_file):
    """Tüm veri satırlarını okur."""
    content = uploaded_file.getvalue().decode().splitlines()
    rows = []
    for line in content:
        if line.startswith("#"):
            continue
        p = line.strip().split("\t")
        rows.append({
            "CHROM": p[0],
            "POS": int(p[1]),
            "REF": p[3],
            "ALT": p[4]
        })
    return pd.DataFrame(rows)

# Streamlit UI
st.set_page_config(page_title="Genetik Varyant Yorumlama", layout="wide")
st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")
st.markdown("### ⚙️ Ayarlar")
api_key = st.text_input(
    "Gemini API Key’iniz",
    type="password",
    help="Kendi anahtarınızı buraya yapıştırın"
)

if not api_key:
    st.warning("API anahtarı girilmedi; yorumlama yapamazsınız.")
    st.stop()

uploaded = st.file_uploader("📁 Dosya yükle (.vcf/.vcf.gz/.csv)", type=["vcf","vcf.gz","csv"])

if uploaded:
    if uploaded.name.endswith(".vcf.gz"):
        df = parse_vcf_gz(uploaded)
    elif uploaded.name.endswith(".vcf"):
        df = parse_vcf(uploaded)
    else:
        df = pd.read_csv(uploaded)

    # --- BURAYA EKLEYİN ---
    required_cols = {"CHROM", "POS", "REF", "ALT"}
    if not required_cols.issubset(df.columns):
        st.error(
            "❌ Yüklenen dosya gerekli sütunları içermiyor:\n"
            "- CHROM\n"
            "- POS\n"
            "- REF\n"
            "- ALT\n\n"
            "Lütfen doğru formatta (.vcf/.vcf.gz veya CSV) ve bu sütunları içeren bir dosya yükleyin."
        )
        st.stop()

    if st.button("🔎 Gemini ile Yorumla"):
        if not api_key:
            st.error("❌ Lütfen önce sidebar’dan API anahtarınızı girin.")
            st.stop()
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

                # PubMed (cache’li)
                pm_response = get_pubmed_ids_cached(str(int(row["ID"])))

                if isinstance(pm_response, dict) and "error" in pm_response:
                    st.warning(f"⚠️ PubMed fetch error for ID {row['ID']}: {pm_response['error']}")
                    pmids = []
                else:
                    pmids = pm_response

                gnomad_response = fetch_gnomad_cached(row["CHROM"], row["POS"], row["REF"], row["ALT"])
                if isinstance(gnomad_response, dict) and "error" in gnomad_response:
                    st.warning(f"⚠️ gnomAD fetch error for variant {row['CHROM']}-{row['POS']}-{row['REF']}-{row['ALT']}: {gnomad_response['error']}")
                    stats = {}
                else:
                    stats = gnomad_response

                # Prompt
                prompt = f"""
You are a clinical geneticist. Based on the following variant and annotation data, provide a professional clinical interpretation.

🧬 Variant:
- Chr: {row['CHROM']}, Pos: {row['POS']}, {row['REF']}→{row['ALT']}

📑 ClinVar:
- Gene: {row.get('GENE','N/A')}, Sig: {row.get('CLNSIG','N/A')}, Dis: {row.get('DISEASE','N/A')}

🧪 ClinGen Validity: {row.get('ClinGen_Validity','N/A')}

st.write(f"📚 PubMed: {', '.join(pmids) if pmids else 'None'}")

📊 gnomAD:
- Exome AC/AN: {stats.get('Exome_AC','N/A')}/{stats.get('Exome_AN','N/A')}
- PopMax AF: {stats.get('PopMax_AF','N/A')} (Pop: {stats.get('PopMax_Pop','N/A')})

🩺 Answer:
1. Likely pathogenicity?
2. Known disease?
3. Clinical relevance?
4. Plain-language summary (≤5 sents).
"""
                try:
                    yorum = generate_with_gemini(prompt, api_key=api_key)
                except Exception as e:
                    yorum = f"❌ {e}"

                results.append({
                    **row.to_dict(),
                    "PubMed_Links": pmids,
                    **stats,
                    "Gemini_Yorum": yorum
                })
                time.sleep(0.3)

        st.success("✅ Tamamlandı")
        st.subheader("📊 Sonuçlar")
        st.dataframe(pd.DataFrame(results))
