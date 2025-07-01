import pandas as pd

def load_clingen_validity(path="Clingen-Gene-Disease-Summary-2025-07-01.csv"):
    try:
        df_raw = pd.read_csv(path, header=None)
        df = df_raw.iloc[5:]  # 6. satırdan itibaren veri
        df.columns = df_raw.iloc[4]  # Gerçek başlıkları 5. satırdan al
        df = df[["GENE SYMBOL", "DISEASE LABEL", "CLASSIFICATION"]].dropna()
        return df
    except Exception as e:
        print("ClinGen dosyası okunamadı:", e)
        return pd.DataFrame()

def get_clingen_classification(gene_symbol, df_clingen):
    gene_row = df_clingen[df_clingen["GENE SYMBOL"] == gene_symbol]
    if not gene_row.empty:
        return gene_row.iloc[0]["CLASSIFICATION"]
    return "Yok"
