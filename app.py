import os
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import gzip, io, time

from pdf_report_generator import create_pdf_report_for_streamlit
from clinvar_parser import enrich_clinvar_df, add_gnomad_links, fetch_gnomad_simple
from gemini_handler import generate_with_gemini
from clingen_handler import load_clingen_validity, get_clingen_classification
from pubmed_handler import get_pubmed_ids_from_clinvar, build_pubmed_links

# Sayfa yapilandirmasi
st.set_page_config(page_title="Genetik App", layout="wide")

# Session state icin key'leri tanimla
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False
if 'results_data' not in st.session_state:
    st.session_state.results_data = None
if 'pdf_created' not in st.session_state:
    st.session_state.pdf_created = False

# — Sidebar'daki sik menu —
with st.sidebar:
    selected = option_menu(
        menu_title="📑 Menu",
        options=["Uygulama", "Dokumantasyon"],
        icons=["house", "file-earmark-text"],
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

if selected == "Dokumantasyon":
    from docs import show_documentation
    show_documentation()
else:
    # Cache'lenmis fonksiyonlar
    @st.cache_data(ttl=24 * 3600, show_spinner=False)
    def get_pubmed_ids_cached(variation_id: str):
        return get_pubmed_ids_from_clinvar(variation_id)

    @st.cache_data(ttl=24 * 3600, show_spinner=False)
    def fetch_gnomad_cached(chrom: str, pos: str, ref: str, alt: str):
        return fetch_gnomad_simple(chrom, pos, ref, alt)

    # Veri yukleme ve hazirlik
    clinvar_df = enrich_clinvar_df(pd.read_parquet("sampled_100.parquet"))
    clinvar_df = add_gnomad_links(clinvar_df, genome_build="GRCh38")
    clingen_df = load_clingen_validity("Clingen-Gene-Disease-Summary-2025-07-01.csv")

    def parse_vcf_gz(uploaded_file):
        rows = []
        with gzip.open(io.BytesIO(uploaded_file.read()), 'rt') as f:
            for line in f:
                if line.startswith("#"): continue
                p = line.strip().split("\t")
                rows.append({"CHROM": p[0], "POS": int(p[1]), "REF": p[3], "ALT": p[4]})
        return pd.DataFrame(rows)

    def parse_vcf(uploaded_file):
        content = uploaded_file.getvalue().decode().splitlines()
        rows = []
        for line in content:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            rows.append({"CHROM": p[0], "POS": int(p[1]), "REF": p[3], "ALT": p[4]})
        return pd.DataFrame(rows)

    # Ana Uygulama
    st.title("🧬 Gemini Destekli Genetik Varyant Yorumlama")

    if st.session_state.analysis_completed and st.session_state.results_data is not None:
        results_df = pd.DataFrame(st.session_state.results_data)
        st.success("✅ Analiz tamamlandi!")

        if st.button("🔄 Yeni Analiz Yap", type="secondary"):
            st.session_state.analysis_completed = False
            st.session_state.results_data = None
            st.session_state.pdf_created = False
            st.rerun()

        tab1, tab2, tab3 = st.tabs(["📊 Sonuclar", "📄 PDF Rapor", "📈 İstatistikler"])

        # Sonuclar Tab
        with tab1:
            st.subheader("📊 Analiz Sonuclari")
            st.dataframe(results_df)
            csv_data = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Sonuclari CSV Olarak İndir",
                data=csv_data,
                file_name=f"genetic_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        # PDF Rapor Tab
        with tab2:
            st.subheader("📄 Profesyonel PDF Rapor")

            if st.session_state.pdf_created:
                st.success("✅ PDF raporu hazir!")
                st.download_button(
                    label="📥 PDF Raporu İndir",
                    data=st.session_state['pdf_bytes'],
                    file_name=st.session_state['pdf_filename'],
                    mime="application/pdf"
                )

                with st.expander("📋 Rapor Detaylari", expanded=True):
                    patient_info = st.session_state.get('pdf_patient_info', {})
                    report_options = st.session_state.get('pdf_report_options', {})
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Hasta Bilgileri:**")
                        st.write(f"- ID: {patient_info.get('id', 'N/A')}")
                        st.write(f"- Ad: {patient_info.get('name', 'N/A')}")
                        st.write(f"- Yas: {patient_info.get('age', 'N/A')}")
                        st.write(f"- Test Tarihi: {patient_info.get('test_date', 'N/A')}")
                    with col2:
                        st.write("**Rapor Ayarlari:**")
                        st.write(f"- Tip: {report_options.get('template', 'N/A')}")
                        st.write(f"- Dil: {report_options.get('language', 'N/A')}")
                        st.write(f"- Grafikler: ✓")
                        st.write(f"- Detayli Analiz: ✓")
            else:
                with st.container():
                    st.info("📝 PDF raporu olusturmak icin formu doldurun.")
                with st.form("pdf_generation_form"):
                    st.markdown("#### 👤 Hasta Bilgileri")
                    col1, col2 = st.columns(2)
                    with col1:
                        patient_id = st.text_input("Hasta ID")
                        patient_name = st.text_input("Hasta Adi")
                    with col2:
                        patient_age = st.number_input("Yas", min_value=0, max_value=150)
                        test_date = st.date_input("Test Tarihi", value=pd.Timestamp.now().date())
                    submitted = st.form_submit_button("🎯 PDF Raporu Olustur")
                    if submitted:
                        with st.spinner("🔄 PDF hazirlaniyor..."):
                            patient_info = {
                                'id': patient_id or f"RPT_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}" ,
                                'name': patient_name or "Belirtilmemis",
                                'age': str(patient_age) if patient_age > 0 else "Belirtilmemis",
                                'test_date': test_date.strftime('%d.%m.%Y')
                            }
                            report_options = {
                                'template': "Özet Rapor",
                                'language': "Turkce",  # Artik kullanicidan secilmiyor, sabit
                                'include_charts': True,
                                'include_detailed_analysis': True
                            }
                            pdf_bytes = create_pdf_report_for_streamlit(results_df, patient_info, report_options)
                            st.session_state['pdf_bytes'] = pdf_bytes
                            st.session_state['pdf_filename'] = f"genetic_report_{patient_info['id']}.pdf"
                            st.session_state.pdf_created = True
                            st.session_state['pdf_patient_info'] = patient_info
                            st.session_state['pdf_report_options'] = report_options
                        st.rerun()

        # İstatistikler Tab
        with tab3:
            st.subheader("📈 Analiz İstatistikleri")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Toplam Varyant", len(results_df))
            with col2:
                pathogenic_count = len(results_df[results_df['CLNSIG'].str.contains('Pathogenic', na=False)])
                st.metric("Pathogenic", pathogenic_count)
            with col3:
                benign_count = len(results_df[results_df['CLNSIG'].str.contains('Benign', na=False)])
                st.metric("Benign", benign_count)
            with col4:
                uncertain_count = len(results_df[results_df['CLNSIG'].str.contains('Uncertain', na=False)])
                st.metric("Uncertain", uncertain_count)
            if 'CLNSIG' in results_df.columns:
                st.subheader("🔍 Klinik Önem Dagilimi")
                st.bar_chart(results_df['CLNSIG'].value_counts())
            if 'GENE' in results_df.columns:
                st.subheader("🧬 En Sık Görulen Genler")
                st.bar_chart(results_df['GENE'].value_counts().head(10))

    else:
        # İlk analiz ekrani
        st.markdown("### ⚙️ Ayarlar")
        api_key = st.text_input("Gemini API Key'iniz", type="password")
        if not api_key:
            st.warning("⚠️ API anahtari girilmedi;")
            st.info("💡 Google AI Studio'dan ucretsiz anahtar alabilirsiniz.")
            st.stop()
        uploaded = st.file_uploader("📁 Dosya yukle (.vcf/.vcf.gz/.csv)", type=["vcf","vcf.gz","csv"])
        if uploaded:
            if uploaded.name.endswith(".vcf.gz"):
                df = parse_vcf_gz(uploaded)
            elif uploaded.name.endswith(".vcf"):
                df = parse_vcf(uploaded)
            else:
                df = pd.read_csv(uploaded)
            required_cols = {"CHROM","POS","REF","ALT"}
            if not required_cols.issubset(df.columns):
                st.error("❌ Yukleme hatasi: gerekli sutunlar eksik.")
                st.stop()
            st.success(f"✅ Dosya yuklendi: {len(df)} varyant.")
            with st.expander("📋 Varyantlari Göster", expanded=False):
                st.dataframe(df.head(20))
            if st.button("🔎 Gemini ile Yorumla", type="primary"):
                with st.spinner("🧠 Yorum yapiliyor..."):
                    for c in ["CHROM","POS","REF","ALT"]:
                        df[c] = df[c].astype(str)
                        clinvar_df[c] = clinvar_df[c].astype(str)
                    merged = pd.merge(df, clinvar_df, on=["CHROM","POS","REF","ALT"], how="left")
                    merged["ClinGen_Validity"] = merged["GENE"].apply(lambda g: get_clingen_classification(g, clingen_df))
                    matched = merged[~merged["ID"].isna()].copy()
                    if matched.empty:
                        st.warning("⚠️ Eslesen varyant yok.")
                        st.stop()
                    st.write(f"✅ {len(matched)} eslesme bulundu.")
                    with st.expander("🔍 Eslesmeleri Göster", expanded=True):
                        st.dataframe(matched.head(30))
                    status = st.empty()
                    overall_pb = st.progress(0)
                    total = len(matched)
                    results = []
                    for idx, (i,row) in enumerate(matched.iterrows(),1):
                        status.markdown(f"### 🔍 İsleniyor {idx}/{total}: {row['CHROM']}:{row['POS']} {row['REF']}>{row['ALT']}")
                        pm_response = get_pubmed_ids_cached(str(int(row["ID"])))
                        pmids = pm_response if not(isinstance(pm_response,dict) and "error" in pm_response) else []
                        gnomad_response = fetch_gnomad_cached(row["CHROM"],row["POS"],row["REF"],row["ALT"])
                        stats = gnomad_response if not(isinstance(gnomad_response,dict) and "error" in gnomad_response) else {}
                        prompt = f"""
You are a clinical geneticist. Based on the following variant and annotation data, provide a professional clinical interpretation.

🧬 Variant:
- Chr: {row['CHROM']}, Pos: {row['POS']}, {row['REF']}→{row['ALT']}

📑 ClinVar:
- Gene: {row.get('GENE','N/A')}, Sig: {row.get('CLNSIG','N/A')}, Dis: {row.get('DISEASE','N/A')}

🧪 ClinGen Validity: {row.get('ClinGen_Validity','N/A')}

📚 PubMed: {', '.join(pmids) if pmids else 'None'}

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
                            yorum = f"❌ Hata: {e}"
                        pubmed_links = build_pubmed_links(pmids)
                        results.append({**row.to_dict(),"PubMed_Links":", ".join(pubmed_links),**stats,"Gemini_Yorum":yorum})
                        time.sleep(0.3)
                        overall_pb.progress(idx/total)
                    st.session_state.results_data = results
                    st.session_state.analysis_completed = True
                    st.rerun()
