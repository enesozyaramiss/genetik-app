import pandas as pd
import re
import requests

def extract_gene(info_str):
    if pd.isna(info_str):
        return None
    match = re.search(r'GENEINFO=([A-Z0-9\-]+)', info_str)
    return match.group(1).split(":")[0] if match else None

def extract_clnsig(info_str):
    if pd.isna(info_str):
        return None
    match = re.search(r'CLNSIG=([^;]+)', info_str)
    return match.group(1) if match else None

def extract_disease(info_str):
    if pd.isna(info_str):
        return None
    match = re.search(r'CLNDN=([^;]+)', info_str)
    return match.group(1).replace("_", " ") if match else None

def extract_rs(info_str):
    if pd.isna(info_str):
        return None
    match = re.search(r'RS=([0-9]+)', info_str)
    return match.group(1) if match else None

def extract_clnvc(info_str):
    if pd.isna(info_str):
        return None
    match = re.search(r'CLNVC=([^;]+)', info_str)
    return match.group(1) if match else None

def extract_clnhgvs(info_str):
    if pd.isna(info_str):
        return None
    match = re.search(r'CLNHGVS=([^;]+)', info_str)
    return match.group(1) if match else None

def extract_clnrevstat(info_str):
    if pd.isna(info_str):
        return None
    match = re.search(r'CLNREVSTAT=([^;]+)', info_str)
    return match.group(1).replace("_", " ") if match else None

def enrich_clinvar_df(df):
    df["GENE"] = df["INFO"].apply(extract_gene)
    df["CLNSIG"] = df["INFO"].apply(extract_clnsig)
    df["DISEASE"] = df["INFO"].apply(extract_disease)
    df["RS"] = df["INFO"].apply(extract_rs)
    df["CLNVC"] = df["INFO"].apply(extract_clnvc)
    df["CLNHGVS"] = df["INFO"].apply(extract_clnhgvs)
    df["CLNREVSTAT"] = df["INFO"].apply(extract_clnrevstat)
    return df

def add_gnomad_links(df, genome_build="GRCh37"):
    import urllib.parse
    def build_url(row):
        chrom = str(row['CHROM']).replace("chr", "").strip()
        pos = int(row['POS'])
        ref = row['REF'].strip(); alt = row['ALT'].strip()
        if not chrom or not ref or not alt:
            return None
        ds = "gnomad_r2_1" if genome_build=="GRCh37" else "gnomad_r4"
        return f"https://gnomad.broadinstitute.org/variant/{chrom}-{pos}-{urllib.parse.quote(ref)}-{urllib.parse.quote(alt)}?dataset={ds}"
    df["gnomAD_Link"] = df.apply(build_url, axis=1)
    return df

def fetch_gnomad_simple(chrom, pos, ref, alt, genome_build="GRCh38"):
    """
    CHROM, POS, REF, ALT bilgisiyle GraphQL üzerinden exome AC/AN ve popmax AF'yi çeker.
    Dönüş: {
      "Exome_AC": int,
      "Exome_AN": int,
      "PopMax_AF": float,
      "PopMax_Pop": str
    } ya da hata/eksikse boş dict.
    """
    url = "https://gnomad.broadinstitute.org/api"
    query = """
    query ($variantId: String!) {
      variant(variantId: $variantId, dataset: gnomad_r4) {
        exome {
          ac
          an
          faf95 { popmax popmax_population }
        }
      }
    }
    """
    vid = f"{chrom}-{pos}-{ref}-{alt}"
    try:
        resp = requests.post(url, json={"query": query, "variables": {"variantId": vid}}, timeout=10)
        data = resp.json().get("data", {}).get("variant")
        ex = data.get("exome", {}) if data else {}
        return {
            "Exome_AC": ex.get("ac"),
            "Exome_AN": ex.get("an"),
            "PopMax_AF": ex.get("faf95", {}).get("popmax"),
            "PopMax_Pop": ex.get("faf95", {}).get("popmax_population"),
        }
    except:
        return {}
