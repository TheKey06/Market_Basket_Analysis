import pandas as pd
import os
from pathlib import Path
import hashlib

pd.options.display.float_format = "{:,.2f}".format

base_dir = Path.cwd()

df = pd.read_csv(f"{base_dir}/files/diario_ventas_new.csv", sep=",", low_memory=False)

df[["cliente", "troevendedor", "centrocostos", "unidadnegocios"]] = df[
    ["cliente", "troevendedor", "centrocostos", "unidadnegocios"]
].astype(str)
df["ruta"] = df["ruta"].astype("Int64").astype(str)
df[["cantidad", "cantxunmedida"]] = df[["cantidad", "cantxunmedida"]].astype("Int64")
df["fechafactura"] = pd.to_datetime(df["fechafactura"])

# these dictionaries were made to get all the information for each reference to fill the empty fields
group_dict = (
    df.dropna(subset=["grouptat"])
    .drop_duplicates(subset=["referencia"])
    .set_index("referencia")["grouptat"]
    .to_dict()
)
marca_dict = (
    df.dropna(subset=["tro_e_marca"])
    .drop_duplicates(subset=["referencia"])
    .set_index("referencia")["tro_e_marca"]
    .to_dict()
)
linea_dict = (
    df.dropna(subset=["lineatat"])
    .drop_duplicates(subset=["referencia"])
    .set_index("referencia")["lineatat"]
    .to_dict()
)
nombrereferencia_dict = (
    df.dropna(subset=["nombrereferencia"])
    .drop_duplicates(subset=["referencia"])
    .set_index("referencia")["nombrereferencia"]
    .to_dict()
)

# Replacing the information
# here we replace null values for "0" because they are negative values and it comes for devolutions
# and those caterogical values we replace with NA is because in those sales the 'zona', 'ciclo' and 'ruta' does not apply
# due to those are online sales or belongs to a different area
df.loc[df["porcentajemargen"].isnull(), "porcentajemargen"] = 0

df.loc[df["porcentajedescuento"].isnull(), "porcentajedescuento"] = 0

df.loc[(df["ruta"].isnull(), "ruta")] = "9999"

df.loc[(df["ruta"] == "NA"), "ruta"] = "9999"

df.loc[(df["zona"].isnull()), "zona"] = "999"

df.loc[(df["zona"] == "NaN"), "zona"] = "999"

df.loc[df["ciclo"].isnull(), "ciclo"] = "Online"

df.loc[df["troevendedor"].isnull(), "troevendedor"] = "9999"

df.loc[df["troevendedor"] == "NA", "troevendedor"] = "9999"

# Mapping the dictionary group to full fill it based on the references
df["grouptat"] = df["grouptat"].fillna(df["referencia"].map(group_dict))
# These part of here are exceptions because there were not found in the dictionary
df.loc[df["grouptat"].isnull(), "grouptat"] = "OTROS"

# Mapping the dictionary brand to full fill it based on the references
df["tro_e_marca"] = df["tro_e_marca"].fillna(df["referencia"].map(marca_dict))
# This if the brand was not found

df.loc[df["tro_e_marca"].isnull(), "tro_e_marca"] = "OTROS"
# Mapping the lineatat to full fill

df["lineatat"] = df["lineatat"].fillna(df["referencia"].map(linea_dict))
# this if the line was not found
df.loc[(df["lineatat"].isnull()) | (df["lineatat"] == "NA"), "lineatat"] = "OTROS"

def hashing_references_recipt(df):
    df_clean = df.copy()

    # setting the identification as a hash code
    def id_anonymous(identificacion):
        return hashlib.sha256(identificacion.encode()).hexdigest()[:10]

    # 1. hashing IDs
    if "cliente" in df_clean.columns:
        df_clean["cliente"] = df_clean["cliente"].apply(id_anonymous)

    if "troevendedor" in df_clean.columns:
        df_clean["troevendedor"] = df_clean["troevendedor"].apply(id_anonymous)

    # 2. Mapping references
    if "referencia" in df_clean.columns:
        refs_unicas = df_clean["referencia"].unique()
        mapa_refs = {ref: f"REF_{i+1:04d}" for i, ref in enumerate(refs_unicas)}
        df_clean["referencia"] = df_clean["referencia"].map(mapa_refs)

    # 3. Mapping receipts
    if "factura" in df_clean.columns:
        facts_unicas = df_clean["factura"].unique()
        mapa_facts = {fact: f"FAC_{i+1:06d}" for i, fact in enumerate(facts_unicas)}
        df_clean["factura"] = df_clean["factura"].map(mapa_facts)

    return df_clean

# 1. Getting the brands we sell sorting by sale
ranking_marcas = (
    df.groupby("tro_e_marca")["montoventapesos"]
    .sum()
    .sort_values(ascending=False)
    .index
)

# dynamic dictionary to set the most purchased brand
dynamic_map = {}
for i, marca in enumerate(ranking_marcas):
    if i == 0:
        dynamic_map[marca] = "Own Brand"
    else:
        dynamic_map[marca] = f"Brand {i}"

# 3. replace brands in the dataframe
df["tro_e_marca"] = df["tro_e_marca"].map(dynamic_map)

df = hashing_references_recipt(df)


df = df.drop(columns={"nombrecliente", "troenombrevendedor", "nombrereferencia"})

df.to_parquet(f"{base_dir}/files/sales.parquet")
