def get_gnomad_frequencies(chrom, pos, ref, alt):
    variant_id = f"{chrom}-{pos}-{ref}-{alt}"
    query = f"""
    {{
      variant(variantId: "{variant_id}", dataset: gnomad_r2_1) {{
        genome {{
          ac
          an
          af
        }}
        exome {{
          ac
          an
          af
        }}
      }}
    }}
    """

    try:
        response = requests.post(
            "https://gnomad.broadinstitute.org/api",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        print("🔵 Raw Response:")
        print(response.text)

        json_data = response.json()

        if "errors" in json_data:
            return {
                "variant_id": variant_id,
                "gnomad_genome_af": None,
                "gnomad_exome_af": None,
                "error": json_data["errors"]
            }

        variant_data = json_data.get("data", {}).get("variant", {})
        genome = variant_data.get("genome") or {}
        exome = variant_data.get("exome") or {}

        return {
            "variant_id": variant_id,
            "gnomad_genome_af": genome.get("af"),
            "gnomad_exome_af": exome.get("af")
        }

    except Exception as e:
        return {
            "variant_id": variant_id,
            "gnomad_genome_af": None,
            "gnomad_exome_af": None,
            "error": str(e)
        }
