import requests

def get_pubmed_ids_from_clinvar(variation_id):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    params = {
        "dbfrom": "clinvar",
        "db": "pubmed",
        "id": variation_id,
        "retmode": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        linksets = data.get("linksets", [])
        if not linksets or "linksetdbs" not in linksets[0]:
            return []
        pmids = []
        for db in linksets[0]["linksetdbs"]:
            if db["dbto"] == "pubmed":
                pmids.extend(db["links"])
        return pmids
    except:
        return []

def build_pubmed_links(pmid_list):
    return [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in pmid_list]