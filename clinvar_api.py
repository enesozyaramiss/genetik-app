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
