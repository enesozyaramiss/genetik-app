# === clinvar_api.py ===
import requests

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

