API KEY = ""
mkdir .streamlit
notepad secrets.toml

# Gemini-Powered Genetic Variant Interpretation

A Streamlit application that integrates ClinVar, ClinGen and gnomAD data to annotate genetic variants from a VCF file, fetch relevant PubMed literature, retrieve allele frequency statistics via gnomAD’s GraphQL API, and generate concise clinical summaries using the Gemini LLM.

---

## Features

- **VCF/VCF.GZ/CSV Input**  
  Upload your variant file; parses the first 200–300 records automatically.
- **ClinVar Annotation**  
  Extracts GENE, CLNSIG (clinical significance), DISEASE, RS, CLNVC, CLNHGVS, CLNREVSTAT from INFO fields.
- **ClinGen Validity**  
  Classifies gene–disease validity using the ClinGen CSV resource.
- **PubMed Links**  
  Retrieves PubMed IDs for each ClinVar Variation ID and builds clickable links.
- **gnomAD Frequency Data**  
  Queries the gnomAD GraphQL API for exome AC/AN and PopMax allele frequency/population.
- **Gemini LLM Interpretation**  
  Feeds all annotations into Gemini to produce a professional clinical interpretation and plain-language summary.

---

Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

Install dependencies:
pip install -r requirements.txt

Run the Streamlit app:
streamlit run app.py

File Structure
├── app.py                   # Streamlit UI and main workflow
├── clinvar_parser.py        # ClinVar INFO parsing & gnomAD link generator
├── clingen_handler.py       # ClinGen CSV loader & classification
├── pubmed_handler.py        # PubMed ID fetcher & link builder
├── gemini_handler.py        # Gemini LLM integration
├── requirements.txt         # Python dependencies
├── README.md                # Project overview (this file)
└── LICENSE                  # MIT License

## License
This project is licensed under the MIT License