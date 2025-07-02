import pandas as pd
import re

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
