import pandas as pd
import os
from pathlib import Path

pd.options.display.float_format = '{:,.2f}'.format

base_dir = Path.cwd()

df = pd.read_csv(f'{base_dir}/files/diario_ventas_new.csv', sep=',',low_memory=False)

df[['cliente','troevendedor']] =df[['cliente','troevendedor']].astype(str)
df['ruta'] = df['ruta'].astype('Int64').astype(str)
variables_categoricas = ['centrocostos','unidadnegocios']
df[['cantidad','cantxunmedida']] = df[['cantidad','cantxunmedida']].astype('Int64')
df['fechafactura'] = pd.to_datetime(df['fechafactura'])

df[variables_categoricas] = df[variables_categoricas].astype(str)

# these dictionaries were made to get all the information for each reference to fill the empty fields
group_dict = (
    df.dropna(subset=["grouptat"])
    .drop_duplicates(subset = ['referencia'])
    .set_index("referencia")['grouptat']
    .to_dict()
)
marca_dict = (
    df.dropna(subset=["tro_e_marca"])
    .drop_duplicates(subset = ['referencia'])
    .set_index("referencia")['tro_e_marca']
    .to_dict()
)
linea_dict = (
    df.dropna(subset=["lineatat"])
    .drop_duplicates(subset = ['referencia'])
    .set_index("referencia")['lineatat']
    .to_dict()
)
nombrereferencia_dict = (
    df.dropna(subset=["nombrereferencia"])
    .drop_duplicates(subset = ['referencia'])
    .set_index("referencia")['nombrereferencia']
    .to_dict()
)

# Replacing the information
# here we replace null values for "0" because they are negative values and it comes for devolutions
# and those caterogical values we replace with NA is because in those sales the 'zona', 'ciclo' and 'ruta' does not apply
# due to those are online sales or belongs to a different area
df.loc[df['porcentajemargen'].isnull(), 'porcentajemargen'] = 0

df.loc[df['porcentajedescuento'].isnull(), 'porcentajedescuento'] = 0

df.loc[(df['ruta'].isnull(), 'ruta')] = '9999'

df.loc[(df['ruta']== 'NA'),'ruta'] = '9999'

df.loc[(df['zona'].isnull()), 'zona'] = '999'

df.loc[(df['zona']== 'NaN'), 'zona'] = '999'

df.loc[df['ciclo'].isnull(), 'ciclo'] = 'Online'

df.loc[df['troevendedor'].isnull(), 'troevendedor'] = '9999'

df.loc[df['troevendedor']== 'NA', 'troevendedor'] = '9999'

# Filling the information with the dictionaries we did before
df['grouptat'] = df['grouptat'].fillna(
    df['referencia'].map(group_dict)
)
# These part of here are exceptions because there were not found in the dictionary
df.loc[df['grouptat'].isnull(),'grouptat'] = 'otros'


df['tro_e_marca'] = df['tro_e_marca'].fillna(
    df['referencia'].map(marca_dict)
)
df.loc[df['tro_e_marca'].isnull(),'tro_e_marca'] = 'OTROS'

df['lineatat'] = df['lineatat'].fillna(
    df['referencia'].map(linea_dict)
)
df.loc[(df['lineatat'].isnull())|(df['lineatat']== 'NA'),'lineatat'] = 'OTROS'

df['nombrereferencia'] = df['nombrereferencia'].fillna(
    df['referencia'].map(nombrereferencia_dict)
)

df.to_parquet(f'{base_dir}/files/sales.parquet')


