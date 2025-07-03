import requests
import logging

logger = logging.getLogger(__name__)

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
            logger.warning(f"No PubMed links found for ClinVar ID {variation_id}")
            return []
        pmids = []
        for db in linksets[0]["linksetdbs"]:
            if db["dbto"] == "pubmed":
                pmids.extend(db["links"])
        return pmids
    except requests.exceptions.RequestException as req_err:
        logger.error(f"HTTP error fetching PubMed IDs for {variation_id}: {req_err}")
        return {'error': f"HTTP error: {req_err}"}
    except ValueError as val_err:
        logger.error(f"JSON decode error for PubMed response {variation_id}: {val_err}")
        return {'error': f"JSON decode error: {val_err}"}
    except Exception as e:
        logger.error(f"Unexpected error in PubMed handler for {variation_id}: {e}")
        return {'error': f"Unexpected error: {e}"}


def build_pubmed_links(pmid_list):
    return [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in pmid_list]