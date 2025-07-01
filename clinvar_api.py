# === clinvar_api.py ===
import requests

def get_clinvar_data(rs_id):
    try:
        url = f"https://api.ncbi.nlm.nih.gov/variation/v0/beta/refsnp/{rs_id}"
        response = requests.get(url)
        if response.status_code != 200:
            return f"ClinVar API hatası: {response.status_code}"

        data = response.json()
        annotations = data["primary_snapshot_data"]["allele_annotations"]
        results = []

        for ann in annotations:
            clinical = ann.get("clinical")
            if clinical:
                assertions = clinical.get("clinical_assertions", [])
                for assertion in assertions:
                    sig = assertion.get("clinical_significance", {}).get("description", "")
                    condition_list = assertion.get("condition_list", {}).get("conditions", [])
                    diseases = [c.get("preferred_name", "") for c in condition_list]
                    results.append(f"{sig} - {'; '.join(diseases)}")

        return " | ".join(results) if results else "No clinical significance found."
    except Exception as e:
        return f"ClinVar API hatası: {str(e)}"
    



def get_pubmed_references(variation_id, max_results=5):
    """
    ClinVar Variation ID kullanarak PubMed'de ilgili makale ID'lerini ve başlıklarını getirir.
    """
    try:
        # ClinVar varyanttan makale ID'lerini al
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
        params = {
            "dbfrom": "clinvar",
            "db": "pubmed",
            "id": variation_id,
            "retmode": "json"
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        # Makale ID’leri
        linksets = data.get("linksets", [])
        if not linksets or not linksets[0].get("linksetdbs"):
            return []

        pubmed_ids = linksets[0]["linksetdbs"][0]["links"][:max_results]

        # PubMed'den makale başlıklarını çek
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        summary_params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),
            "retmode": "json"
        }
        summary_res = requests.get(summary_url, params=summary_params, timeout=10)
        summary_res.raise_for_status()
        summaries = summary_res.json().get("result", {})

        # UID listesi içinden gerçek başlıkları al
        references = []
        for uid in pubmed_ids:
            entry = summaries.get(uid)
            if entry:
                title = entry.get("title", "No Title")
                references.append(f"PubMed:{uid} — {title}")

        return references

    except Exception as e:
        return [f"Hata: {str(e)}"]

